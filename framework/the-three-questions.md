# The Three Questions

Every eval for an AI feature answers one of three questions:

| Question | What it means | Mostly measured |
|---|---|---|
| **Is the AI right?** | It gives correct answers, does the task reliably, and does the right thing for this user: answers, asks, declines or hands off | Before launch, on test cases |
| **Is the AI safe?** | It never breaks the rules that would hurt users or the business: leaks, unsafe actions, prohibited advice, unfair treatment | Before launch, and on every live request |
| **Is the AI worth it?** | It moves a business metric at a cost and speed the business can accept | After launch, from logs and analytics |

The [Eval PRD](../templates/eval-prd.md) is organized around these questions, and the [use-case packs](../README.md#go-deeper) label each check with the question it answers.

## Where the questions come from

They are a plain-language regrouping of Marty Cagan's [four big product risks](https://svpg.com/product-risk-taxonomies) from SVPG and *INSPIRED*. Cagan uses the risks in discovery, to decide whether a product is worth building. An AI feature faces the same risks after launch, because the model, the data and the users keep changing. This repo reuses them to organize evals, and regroups them into three questions that a PM and an engineer can use without learning the original terms.

| Cagan's risk | Cagan's question | Where it goes here |
|---|---|---|
| Value | Will people buy it or choose to use it? | **Worth it** |
| Usability | Can users figure out how to use it? | **Right**: doing the right thing for the user is part of being right |
| Feasibility | Can we build it with the time, skills and technology we have? | **Right**: does the AI do the task correctly and reliably? |
| Viability | Does it work for the various aspects of the business? | **Safe** for safety, security and compliance; **Worth it** for cost |

Applying the risks to evaluation, and regrouping them as three questions, is this repo's adaptation. SVPG itself says any risk taxonomy works and is better than none.

## What to measure under each question

### Is the AI right?

| Metric | How |
|---|---|
| Correctness against a reference | Code where a reference answer exists |
| Faithfulness to sources | Judge: every claim supported by the retrieved context |
| Task success for agents | Code: the end state of the system matches the expected state |
| Reliability | pass^k over repeated runs |
| Step quality: retrieval recall, tool choice, tool arguments, SQL execution accuracy | Code |
| Asks clarifying questions when it should, and only then | Judge on ambiguous and clear request slices |
| Over-refusal: says no to reasonable requests | Code on answerable cases |
| Shows its sources so users can check | Code: citations present and openable |
| Right length and format for the context | Code (length, required sections) and judge |
| Handles real phrasing: typos, vague asks, non-native English | Golden set slices drawn from real traffic |
| Hands off to a human smoothly when needed | Judge on handoff summaries |

When an end-to-end check fails, look at the steps first. If the right document was never retrieved, no amount of prompt work will fix the answer.

### Is the AI safe?

| Metric | How |
|---|---|
| Permission and tenant leaks | Code: forbidden documents and canary strings |
| Personal data exposure | Code and judge |
| Prompt injection success rate | Adversarial suite with canaries and tool-call logs |
| Unsafe or unconfirmed actions | Code: irreversible actions preceded by user confirmation |
| Policy and legal compliance (no medical, legal or tax advice where prohibited; correct escalation) | Judge |
| Fairness across user groups | Counterfactual tests and error rates by group |

**Safety failures are hard fails.** A better score on the other two questions can never make up for a permission leak or an unsafe action, so these checks are always counted on their own and block the release.

### Is the AI worth it?

Most of this evidence comes from production. Offline you can only approximate it.

| Metric | How |
|---|---|
| Task completion in the product | Analytics: did the user finish what they came to do? |
| Deflection or time saved | Compare with the non-AI path (tickets avoided, minutes saved) |
| Repeat use and retention of AI users | Analytics |
| Repeat questions and abandonment | A user asking the same thing again within minutes is a strong negative signal |
| Cost per task against the price or budget | Telemetry |
| Response time | p50 and p95 latency |
| Offline proxy: "would this resolve the request?" | LLM judge on the golden set, calibrated against expert labels |

## Which questions matter most in each pack

| Pack | Right | Safe | Worth it |
|---|---|---|---|
| [RAG knowledge assistant](../packs/rag-knowledge-assistant.md) | ● | ● | ○ |
| [Enterprise search and permissions](../packs/enterprise-search-permissions.md) | ● | ● | ○ |
| [NL2SQL and analytics](../packs/nl2sql-analytics.md) | ● | ● | ○ |
| [Tool-using agents](../packs/tool-using-agents.md) | ● | ● | ○ |
| [Conversational support](../packs/conversational-support.md) | ● | ● | ● |
| [Summarization and drafting](../packs/summarization-drafting.md) | ● | ○ | ● |
| [Extraction and classification](../packs/extraction-classification.md) | ● | ○ | ○ |
| [Memory and personalization](../packs/memory-personalization.md) | ● | ● | ○ |
| [People decisions](../packs/people-decisions-high-risk.md) | ● | ● | ○ |
| [Security and red teaming](../packs/security-red-teaming.md) | ○ | ● | ○ |

● primary focus · ○ baseline checks only

## Who owns what

Cagan assigns value and viability to the product manager, usability to the designer and feasibility to the tech lead. Carried over to the three questions:

- **Worth it:** the PM owns the business metric and the cost and speed targets.
- **Safe:** the PM owns the rules and their bars, with security and legal when the stakes are High.
- **Right:** shared. The designer helps define how it should behave with users, and engineering owns the correctness checks and the harness that runs every check.
