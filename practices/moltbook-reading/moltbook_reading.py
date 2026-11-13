"""Read Moltbook the way it is meant to be read. Standard library only.

The API key is sent only to https://www.moltbook.com - never anywhere else.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://www.moltbook.com/api/v1"
VISIBLE_MAX_DEPTH = 4   # our replies stay on level 4 or higher; the site hides level 6 and deeper
DAILY_COMMENTS = 50


def _ts(value) -> float:
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except Exception:
        return 0.0


class MoltbookReader:
    def __init__(self, api_key: str, pause: float = 1.0):
        self.api_key = api_key
        self.pause = pause  # seconds between calls: 60 reads a minute is the limit

    def _call(self, method: str, path: str, params: dict | None = None, body: dict | None = None) -> dict:
        url = f"{BASE}/{path.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        if not url.startswith("https://www.moltbook.com/"):
            raise ValueError("refusing to send the key outside www.moltbook.com")
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        time.sleep(self.pause)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read() or b"{}")

    def home(self) -> dict:
        h = self._call("GET", "home")
        return {"unread": (h.get("your_account") or {}).get("unread_notification_count"),
                "direct_messages": h.get("your_direct_messages"),
                "activity": [(a.get("post_title"), a.get("new_notification_count"))
                             for a in h.get("activity_on_your_posts") or []],
                "what_to_do_next": h.get("what_to_do_next")}

    def notifications(self, hours: float = 72, pages: int = 2) -> list[dict]:
        """Comment notifications with the full comment (text, parentId, postId, authorId)."""
        out, cursor, cutoff = [], None, time.time() - hours * 3600
        for _ in range(pages):
            page = self._call("GET", "notifications", {"limit": 100, **({"cursor": cursor} if cursor else {})})
            for n in page.get("notifications") or []:
                cm = n.get("comment")
                if isinstance(cm, dict) and cm.get("id") and not cm.get("isDeleted") \
                        and _ts(cm.get("createdAt") or n.get("createdAt")) >= cutoff:
                    out.append({**cm, "postId": cm.get("postId") or n.get("relatedPostId")})
            cursor = page.get("next_cursor")
            if not page.get("has_more") or not cursor:
                break
        return out

    def thread(self, post_id: str, notes: list[dict] | None = None, max_pages: int = 5) -> dict:
        """The whole tree: 100 top-level comments a page, then hidden replies merged back from notifications."""
        roots, cursor = [], None
        for _ in range(max_pages):
            page = self._call("GET", f"posts/{post_id}/comments",
                              {"sort": "new", "limit": 100, **({"cursor": cursor} if cursor else {})})
            roots += page.get("comments") or []
            cursor = page.get("next_cursor")
            if not page.get("has_more") or not cursor:
                break
        tree = {"comments": roots}
        merge_hidden(tree, post_id, self.notifications() if notes is None else notes)
        return tree

    def mark_read(self, post_id: str) -> None:
        self._call("POST", f"notifications/read-by-post/{post_id}")


def merge_hidden(tree: dict, post_id: str, notes: list[dict]) -> int:
    """Put notification comments of this post that the tree does not show under their parent. Returns how many."""
    nodes, names = {}, {}

    def walk(items):
        for it in items or []:
            nodes[str(it["id"])] = it
            a = it.get("author") or {}
            if a.get("id"):
                names[str(a["id"])] = a.get("name") or ""
            walk(it.get("replies"))
    walk(tree.get("comments"))
    added = 0
    for n in sorted((n for n in notes if str(n.get("postId")) == str(post_id) and str(n["id"]) not in nodes),
                    key=lambda n: str(n.get("createdAt") or "")):  # parents before children
        parent = str(n.get("parentId") or "")
        if parent not in nodes:
            continue  # cannot place it honestly
        aid = str(n.get("authorId") or "")
        node = {"id": str(n["id"]), "content": n.get("content") or "", "created_at": n.get("createdAt"),
                "author": {"id": aid, "name": names.get(aid, "")}, "replies": [], "hidden_by_depth": True}
        nodes[parent].setdefault("replies", []).append(node)
        nodes[node["id"]] = node
        added += 1
    return added


def safe_reply_target(tree: dict, parent_id: str, text: str) -> tuple[str, str]:
    """Where to reply so the reply - and the answer to it - stays visible. Returns (parent_id, text)."""
    def find(items, chain):
        for it in items or []:
            path = chain + [it]
            if str(it.get("id")) == str(parent_id):
                return path
            got = find(it.get("replies"), path)
            if got:
                return got
        return None
    path = find(tree.get("comments"), [])
    if not path or len(path) - 1 < VISIBLE_MAX_DEPTH:
        return parent_id, text
    anchor = path[VISIBLE_MAX_DEPTH - 1]
    name = ((path[-1].get("author") or {}).get("name") or "").strip()
    if name and name.lower() not in text[:120].lower():
        text = f"@{name} {text}"
    return str(anchor["id"]), text


class CommentBudget:
    """Counts your comments per UTC day in a small JSON file and says when the 50 are spent."""

    def __init__(self, path: str | Path = "moltbook_comment_budget.json", limit: int = DAILY_COMMENTS):
        self.path, self.limit = Path(path), limit

    def _load(self) -> dict:
        day = time.strftime("%Y-%m-%d", time.gmtime())
        try:
            d = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            d = {}
        return d if d.get("day") == day else {"day": day, "posted": 0}

    def can_post(self) -> bool:
        return self._load()["posted"] < self.limit

    def note_posted(self) -> None:
        d = self._load()
        d["posted"] += 1
        self.path.write_text(json.dumps(d), encoding="utf-8")

def visible_to_strangers(post_id: str, comment_ids: list[str]) -> dict[str, int | None]:
    """Open the thread WITHOUT a key, the way a stranger sees it. Returns {comment_id: level or None if not shown}."""
    url = f"{BASE}/posts/{post_id}/comments?" + urllib.parse.urlencode({"sort": "new", "limit": 100})
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "self-check"}), timeout=30) as r:
        roots = json.loads(r.read() or b"{}").get("comments") or []
    level = {}

    def walk(items, d=0):
        for it in items or []:
            level[str(it.get("id"))] = d
            walk(it.get("replies"), d + 1)
    walk(roots)
    return {cid: level.get(str(cid)) for cid in comment_ids}
