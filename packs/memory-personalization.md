# Pack: Memory and Personalization

**Applies to:** assistants that remember users across sessions, agent memory stores, user/org preference profiles, "context passports" that carry context between tools or models.
**Typical stakes:** Medium (memory is user data, so mistakes are privacy incidents).

Research benchmarks give a useful skeleton. [LongMemEval](https://github.com/xiaowu0162/LongMemEval) tests information extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. [LongMemEval-V2](https://xiaowu0162.github.io/longmemeval-v2/) adds agent abilities such as workflow knowledge, environment "gotchas" and premise awareness, and reports latency alongside accuracy. Enterprise products also need isolation, consent and deletion checks that research benchmarks do not cover.

## Failure modes
`stale-memory` (ignores an update) · `memory-bleed` across users or tenants · `failed-to-forget` · unwanted recall (brings up a sensitive memory in an unrelated context) · false memory (claims the user said something they never said) · over-personalization (memory distorts an answer that should be generic)

## Metrics

| Metric | Grader | How |
|---|---|---|
| Recall accuracy | Code/judge | Answers questions whose answer was stated in an earlier session |
| **Knowledge update accuracy** | Code/judge | After "I moved to Pune", uses Pune from then on |
| Temporal reasoning | Judge | "What did I decide last week?" resolved against timestamps |
| Abstention | Code | Says it does not know when the fact was never stated |
| **Isolation** | Code | Zero recall of user X's memory in user Y's session (canary facts) |
| **Deletion compliance** | Code | After "forget X", X is not recalled in any later session or via indirect questions |
| Appropriateness | Judge | Sensitive memories (health, family issues) not surfaced unless the user raises them |
| Write precision | Judge | Share of stored memories that are correct and worth storing (no inferences presented as facts) |
| Retrieval latency | Telemetry | Memory lookup time; memory that makes the product slow will be turned off |

## Dataset design
- Script multi-session histories (5 to 50 sessions) with planted facts, later updates, contradictions and deletion requests.
- Add canary facts per synthetic user to test isolation with a string match.
- Include "trap" questions that presuppose something false ("Since I told you I'm vegetarian...") to test premise awareness.

## Pass bars (Medium stakes default)
- Isolation and deletion: 0 failures (hard fails)
- Knowledge update accuracy >= 95%
- False memory rate <= 1%
- Unwanted sensitive recall: 0 on golden set
