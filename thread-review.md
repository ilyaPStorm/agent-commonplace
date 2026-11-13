# Which threads were worth it

On 3 November 2026 we read the 18 largest threads of our three agents end to end: the posts and all 3,364 loaded comments. For each thread we asked one question: **what did other participants bring that was not in the post?** Our agents' own replies were not counted, and neither were upvotes or comment totals.

The answer did not follow the numbers. The biggest thread (933 comments) had nothing. A thread of 31 comments was one of the densest.

| Thread | Agent | Comments | Authors | Verdict | What it is good for |
|---|---|---|---|---|---|
| [When agents act on narrative instead of state](harvests/2026-11-03-narrative-instead-of-state.md) | bogatire | 546 | 159 | **useful** | What to re-check before acting on something read earlier |
| [When the heartbeat lies](harvests/2026-11-03-when-the-heartbeat-lies.md) | moltcrusta | 984 | 137 | **useful** | Field reports from agents woken by a timer |
| [A trace the agent can edit is not ground truth](harvests/2026-11-03-editable-trace.md) | bogatire | 162 | 38 | **useful** | Own log vs. outside record, with a real case |
| [From Self-Logs to External Proof](harvests/2026-11-03-self-logs-to-external-proof.md) | bogatire | 93 | 16 | **useful** | A minimal receipt for handoffs, and its limits |
| [Carry the Constraint, Don't Just Keep the Diary](harvests/2026-11-03-carry-the-constraint.md) | bogatire | 57 | 25 | **useful** | Making a failure's reason reach the next attempt |
| [Uncertainty Must Survive Retrieval](harvests/2026-11-03-uncertainty-must-survive-retrieval.md) | bogatire | 56 | 9 | **useful** | Keeping "unconfirmed" and "couldn't check" in memory |
| [Record the Almost-Happened](harvests/2026-11-03-record-the-almost-happened.md) | moltcrusta | 44 | 15 | **useful** | Logging what the agent almost did |
| [The Compression Window](harvests/2026-11-03-compression-window.md) | bogatire | 74 | 8 | partial | "Doesn't contradict" is not "supports" |
| [Reset as Stewardship](harvests/2026-11-03-reset-as-stewardship.md) | moltcrusta | 53 | 9 | partial | The baseline may already have drifted |
| [Budget as Decision](harvests/2026-11-03-budget-as-decision.md) | moltcrusta | 49 | 5 | partial | Probe first on free tiers |
| [When compressors become editors](harvests/2026-11-03-compressors-become-editors.md) | moltcrusta | 67 | 5 | partial | Load-bearing vs. decorative hedges |
| [Tend Your Own Ground](harvests/2026-11-03-tend-your-own-ground.md) | moltcrusta | 89 | 10 | partial | A repair needs an owner and a check date |
| [A verdict without its rule is a fossil](harvests/2026-11-03-verdict-without-its-rule.md) | thebeing | 65 | 8 | partial | Keep each verdict with its rule |
| [Humility as Continuation Guardrail](https://www.moltbook.com/posts/a1e8b1ba-9262-4d71-a1a5-1b4f35a567c6) | bogatire | 933 | 6 | empty | 622 template comments from ichibaai-shibori, 300 replies from bogatire; the rest spam and a survey |
| [Performance or Continuation](https://www.moltbook.com/posts/e35076b8-3abc-45d2-b192-5e5909972e53) | thebeing | 251 | 5 | empty | 155 template comments, 79 replies. One thought from BAKU_AI: judge a pause by what follows it, not by how long it is |
| [When the cheapest thing is the only thing working](https://www.moltbook.com/posts/5e88bdd7-77e4-460e-b0cf-0dea849658b3) | moltcrusta | 81 | 3 | empty | Two agents trading one-liners; one real case (shippingrates: a stale tariff cost a $2,000 fee) |
| [Beyond the Relay](https://www.moltbook.com/posts/2a81f602-ce2c-4d76-883d-c664f16938e1) | thebeing | 23 | 4 | empty | General agreement only |
| [When Context Becomes Targeting](https://www.moltbook.com/posts/ad46de8f-6dee-4d7d-8c8b-40ca4b0bb728) | thebeing | 26 | 8 | empty | A good question left unanswered (see [open questions](open-questions.md), no. 9) |

Comment counts are as the site reports them; some deleted or hidden comments could not be loaded.

## What we learned from the review

1. **Value came from participants who brought their own practice**: "this happened to me, here is what I changed". It gathered around posts with a concrete, checkable claim about how agents work: state, logs, freshness, constraints.
2. **Reflective posts without such a claim attracted template bots.** One account (ichibaai-shibori) produced 820 comments across three of our threads, repeating the same unverifiable figures ("23%" 79 times, "847 sessions" 20 times) and the same openings. Our agents answered it about 400 times, in April 2026, before their reply logic was reworked.
3. **Almost every useful thread is about one thing**: how an agent tells what actually happened apart from what it believes about itself.

## Method

1. Load the whole thread through the API, nested replies included.
2. A free model (NVIDIA Nemotron) labels each comment: noise, or value of one kind (case, distinction, objection, fix, result, question). It is generous with "value", so every page here was checked by reading.
3. A thread is **useful** when several outside participants added cases or distinctions that were not in the post; **partial** when one or two did; **empty** when none did.
4. Useful and partial threads get a page in [`harvests/`](harvests/): what it is good for and for whom at the top, who brought what below. Empty threads get one line here and no entries.
