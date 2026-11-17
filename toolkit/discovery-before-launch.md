# Discovery Before Launch

*Used in the **Discover** stage of [the Loop](../framework/the-loop.md) when you have no production traces yet.*

Most eval guidance starts with "pull your production traces". If you are shipping your first agent, you don't have any yet. You do have something almost as useful: the workflow the agent is going to take over. People and simpler systems have been doing this work for years, and every mistake they made left a record somewhere.

The goal is to build a credible first list of failure modes, a starter golden set and draft ship gates before real users touch the agent. Once you launch, move to trace-based discovery as described in [the Loop](../framework/the-loop.md) and treat this list as a hypothesis to test.

## Step 1: Map the current workflow

Write down how the job gets done today, step by step, along with who does each step and which systems they touch. For each step note:

- The inputs used and where they come from
- The decision being made and the rules or judgment behind it
- What gets checked, by whom, and how often it catches something
- What happens when it goes wrong, and who finds out

This map becomes your task list for the agent and tells you which steps need their own evaluator.

## Step 2: Mine the existing records for failures

Each of these sources describes real failures in your domain. Sample from them the same way you would sample traces.

| Source | What it tells you | Example |
|---|---|---|
| Support and service tickets | The questions people actually ask, in their own words, and which answers caused follow-ups | Tickets reopened after the first reply |
| Escalations and complaints | Cases where the current process failed someone | Complaints escalated to a manager or a specialist team |
| QA and audit findings | Errors reviewers already catch, with severity | Billing audit exceptions, compliance review notes |
| Rework and corrections | Outputs that had to be redone | Offer letters reissued, invoices corrected |
| SOPs, policy docs and checklists | The rules the agent must follow, including the exceptions people forget | Refund policy exceptions by region or plan |
| Training material for new staff | The mistakes the organization expects beginners to make | "Common errors" pages in onboarding guides |
| Search logs and analytics | What users look for and fail to find | Zero-result searches in the help center |
| Existing rule-based or ML systems | Known misroutes and their cost | Ticket router confusion matrix |

Tag what you find with the [failure tags](failure-tags.md), the same way you would tag traces. Most tags will carry over from the human workflow. The agent adds a few failure types of its own, mostly in the tools and actions, grounding and security groups.

## Step 3: Interview the experts doing the work

Thirty minutes with three or four people who do the job today is often worth more than any document. Ask them:

- Which cases are hard, and how do you recognize them?
- What do new team members usually get wrong?
- When do you stop and ask someone, and who?
- What would be embarrassing or dangerous to get wrong?
- What do customers misunderstand most often?

Their answers give you hard fails, escalation rules and the edge cases that are missing from the written policy.

## Step 4: Generate traces before launch

Get real agent behavior to review as early as you can. In rough order of realism:

1. **Replay historical inputs.** Run past tickets, requests or questions through the agent in a sandbox and compare its output with what the human did. This is the closest thing to production traces you can get before launch.
2. **Shadow mode.** Run the agent alongside the live process without showing its output to users. Experts compare the agent's output with their own work.
3. **Internal dogfooding.** Let employees who know the domain use it for real tasks, and review every session.
4. **Simulated users.** Use an LLM user simulator with personas built from Step 2 (confused, terse, frustrated, non-native speaker) and goals taken from real tickets. Use this to scale up coverage. Its realism is limited, so keep it alongside the real inputs above.
5. **Pre-mortem.** Ask the team to imagine the launch went badly six months from now and write down why. Turn each plausible cause into at least one test case.

Review the resulting traces with the [error discovery sheet](../templates/error-discovery-sheet.csv) and the same open-coding process you would use after launch.

## Step 5: Set the human baseline

Measure how well the current process performs on the same golden set: accuracy, time per task, escalation rate, error severity. This gives you an honest bar to ship against. Teams often hold an agent to a near-perfect standard that the existing process has never met, and then never ship. A more useful gate is usually "matches or beats today's process on quality, with zero hard fails, at lower cost or time".

## Step 6: Launch narrowly and switch to traces

- Start with a limited audience, a narrow set of intents, or a human-in-the-loop mode where the agent drafts and a person approves.
- Review traces daily for the first two weeks. Expect to find failure modes that none of the steps above predicted.
- Move confirmed production failures into the regression suite, and retire pre-launch test cases that turn out to be unrealistic.

## Output checklist

- [ ] Workflow map with the decision points marked
- [ ] Failure mode list from historical records and expert interviews, tagged and ranked
- [ ] Starter golden set (50 to 150 cases) built mostly from real historical inputs
- [ ] At least 30 agent traces reviewed from replay, shadow mode or dogfooding
- [ ] Human baseline measured on the golden set
- [ ] Stakes level agreed and draft pass bars in section 7 of the [Eval PRD](../templates/eval-prd.md)
- [ ] Launch plan with a limited scope and a daily trace review owner
