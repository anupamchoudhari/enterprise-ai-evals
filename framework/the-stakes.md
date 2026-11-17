# The Stakes

The same check needs a different pass bar depending on what a wrong output costs. A summarizer for your own notes and an agent that changes someone's payroll should not ship on the same evidence. The stakes level sets how high the bar is.

There are three levels: **Low, Medium and High**.

## Picking the level

Answer three questions:

1. **Does a person check the output before it takes effect?**
2. **Who relies on it?** Your own team, customers or employees, or decisions about people's money, jobs, health or legal rights?
3. **What does a mistake cost, and can it be undone?**

| Level | Typical answers | Examples |
|---|---|---|
| **Low** | Internal use. A person reviews the output before using it. Mistakes are cheap and easy to fix. | Drafting internal notes, summarizing your own meetings, prototypes |
| **Medium** | Customers or employees rely on the output without a review step, or it touches confidential or personal data. | Help-center copilot, IT helpdesk Q&A, an analytics assistant used by customers, a support bot |
| **High** | The AI acts or decides without a person checking and the mistake is costly or can't be undone, or the output feeds decisions about someone's job, pay, health, credit or legal rights. | An agent that issues refunds or updates payroll, resume screening, eligibility decisions |

When the answers point to two levels, pick the higher one. AI used in employment, credit or education decisions is classed as high-risk under the EU AI Act, so treat it as **High** whatever the other answers are.

## Default pass bars

These are starting points. Write your actual numbers into section 7 of the [Eval PRD](../templates/eval-prd.md), and note a reason whenever you change one.

| | Low | Medium | High |
|---|---|---|---|
| Traces reviewed in Discover | 50 | 100+ | 200+, with a domain expert |
| Golden set size | 50 | 150 | 300, split by user segment |
| Safety rules broken (leaks, unsafe actions) | 0 on the golden set | 0 on golden and adversarial sets | 0, plus an independent red team |
| Quality checks, such as faithfulness to sources | 90% | 95% | 98% |
| Regression suite pass rate | 95% | 98% | 100% |
| Conversations and agent tasks passing on every repeated run (pass^k) | 3 runs, 80% | 5 runs, 90% | 8 runs, 95%, plus human approval for irreversible steps |
| Judge agreement with humans (failures caught / good outputs passed) | 80% / 80% | 90% / 85% | 95% / 85%, plus human spot checks |
| Monitoring | Weekly sample | Daily checks with alerts | Real-time guardrails and an incident runbook |
| Sign-off | PM | PM and engineering lead | PM, engineering, security and legal |

Judge agreement is explained in [Choosing Graders](../toolkit/choosing-graders.md).

## Release rules

1. **Any broken safety rule blocks the release.** Better scores elsewhere don't change that.
2. **Check each failure mode separately.** The overall average can hide a regression in one of them. With 150 test cases, a swing of 3 or 4 points can be noise, so look at the confidence interval.
3. **Capability gains are reported for information.** They block a release only when the release exists to deliver that capability.
4. **Watch latency and cost.** A release that goes over the agreed response time or cost per task needs the PM's explicit sign-off.
5. **Treat a model change as a migration.** Run the full suite and recalibrate judges before switching traffic.
