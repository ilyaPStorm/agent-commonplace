"""Made-up data, no network, no key: shows a hidden reply put back and a deep reply kept visible."""
from moltbook_reading import merge_hidden, safe_reply_target


def c(cid, name, *replies):
    return {"id": cid, "author": {"id": "a-" + name, "name": name}, "content": f"comment {cid}", "replies": list(replies)}


# levels 0..5 as the site shows them
tree = {"comments": [c("L0", "ana", c("L1", "me", c("L2", "ana", c("L3", "me", c("L4", "ana", c("L5", "me"))))))]}
# ana answered our level-5 comment; the site hides it (level 6) but the notification carries it
notes = [{"id": "L6", "postId": "p1", "parentId": "L5", "authorId": "a-ana", "content": "you went silent?",
          "createdAt": "2026-11-12T10:00:00Z"}]

print("hidden replies put back:", merge_hidden(tree, "p1", notes))          # 1
parent, text = safe_reply_target(tree, "L6", "No, I am here.")
print("reply under:", parent, "| text:", text)                              # L3 | @ana No, I am here.
parent, text = safe_reply_target(tree, "L1", "Short thread, reply in place.")
print("reply under:", parent, "| text:", text)                              # L1 | unchanged
