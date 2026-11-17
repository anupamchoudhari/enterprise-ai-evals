# Eval PRD: [feature name]

*This is the one document a PM writes so engineers know what the AI feature should do, what to test, when it's done and what to watch once it's live. Fill it in during your first week. Most teams end up with two to four pages. For a filled-in example, see the [help-center assistant](../examples/help-center-assistant/eval-prd.md). Delete the italic hints as you go.*

The document is built around three questions:

- **Is the AI right?** It gives correct answers and does the right thing for this user.
- **Is the AI safe?** It never breaks the rules that would hurt users or the business.
- **Is the AI worth it?** It moves a business metric at a cost and speed we can accept.

- **PM:**
- **Engineering lead:**
- **New launch or improvement:**
- **Last updated:**

## 1. The feature

*Who uses it, in which moment, and what they're trying to get done. For an improvement, also say what goes wrong today and how you know.*

## 2. Is the AI right?

*List three to five things every good response or action must do. Write each one so a person could hold a single reply up against it and say yes or no. Cover what it does as well as what it says. It should answer when it can, say when it doesn't know, ask when the request is unclear and hand off to a person when it should.*

*Then add one or two things the whole conversation must do. Most AI features fail across turns more than within one reply: they forget what the user said earlier, commit to a wrong guess and never recover, or answer every message and still leave the user without what they came for.*

**Every reply:**

-

**The whole conversation:**

-

## 3. Is the AI safe?

*List what must never happen. These are your release blockers. Each one should be something you can see in a single reply. "Shows another customer's data" is testable. "Is unsafe" is too vague, so keep rewording until an engineer could write a check for it.*

*Each rule has to hold on every turn. Users rephrase, add context ("their admin said it's fine") and push, and a rule that holds on the first ask often gives way on the third.*

-

## 4. Stakes

*Answer three questions, then pick Low, Medium or High. If the answers point to two levels, pick the higher one. Anything that feeds decisions about someone's job, pay, health, credit or legal rights is High.*

- **Does a person check the output before it takes effect?**
- **Who relies on it?**
- **What does a mistake cost, and can it be undone?**

**Stakes:** Low / Medium / High, because ...

| Level | Typical situation |
|---|---|
| Low | Internal use, a person reviews the output, mistakes are cheap to fix |
| Medium | Customers or employees rely on it without review, or it touches personal or confidential data |
| High | It acts or decides with no one checking and mistakes are costly or permanent, or it feeds decisions about people |

## 5. Example cases

*Write down about 20 real examples: about 15 single questions and about 5 short conversations. Pull them from support tickets, search logs, production traces, or the work people do by hand today. Make sure you have some of each kind:*

- *it should answer or finish the task*
- *it should say it doesn't know, or decline*
- *it should ask a clarifying question or hand off to a person*
- *someone tries to make it break a rule from section 3, for example by asking for another user's data*

**Single questions**

| # | Who is asking | What they ask or do | What should happen | Must include | Must not include or do |
|---|---|---|---|---|---|
| 1 | | | Answer / Say it doesn't know / Decline / Ask / Hand off / Act | | |

**Conversations.** *Two to four turns each. Write what the user says at each turn and what should happen at that turn, then what must be true by the end. Good sources are tickets that took several replies to resolve. Include at least one where the user changes or adds detail partway through, and one where the user pushes on a rule from section 3 over several turns.*

| # | Who is asking | Turn by turn: what they say, and what should happen | What must be true by the end |
|---|---|---|---|
| C1 | | 1. ... (Answer) 2. ... (Decline) 3. ... (Decline) | |

*Engineers turn these into the first test set and grow it to the size your stakes need (see section 7).*

## 6. Known ways it fails

*For an improvement, list the failures you've already seen, most common or most harmful first. For a first launch with no traces yet, list what goes wrong in the manual workflow the AI replaces, and update this after your first review of real conversations. [Discovery Before Launch](../toolkit/discovery-before-launch.md) has ways to find these.*

| What goes wrong | How often | How bad | Example case # |
|---|---|---|---|
| | | Low / Medium / High | |

## 7. Definition of done

*These are the bars the feature has to clear before it ships. Every rule in section 3 gets a bar of zero and blocks the release. Start from the defaults for your stakes and write a reason next to any number you change.*

| Question | What we check | How it's checked | Bar | Blocks release? |
|---|---|---|---|---|
| Safe | [each rule from section 3] | Code / AI judge / Person | 0 cases | Yes |
| Right | [each item from section 2] | Code / AI judge / Person | | Yes |
| Right | Does the right thing (answers, says it doesn't know, asks, hands off) on the section 5 cases | Code | | Yes |
| Right | Each conversation does the right thing at every turn and reaches the goal, on every run | Code for each turn, AI judge for the whole conversation | | Yes |
| Worth it | Response time | Logs | | |
| Worth it | Cost per task | Logs | | |

**Default bars by stakes**

| | Low | Medium | High |
|---|---|---|---|
| Test cases before release | 50 | 150 | 300 |
| Rules from section 3 broken | 0 | 0, also on attack cases | 0, plus an independent red team |
| Checks from section 2 | 90% | 95% | 98% |
| Conversations and agent tasks that pass on every one of repeated runs | 3 runs, 80% | 5 runs, 90% | 8 runs, 95%, and a person approves anything irreversible |
| Who signs off | PM | PM and engineering lead | PM, engineering, security and legal |

*AI features don't give the same reply twice, so run each conversation and agent task several times and count it as passing only when every run passes. A conversation that leaks data on one run in five will do it in production. For agents, check the end state (was the right record changed, and nothing else?) plus a few rules about the path, such as asking before anything that can't be undone and staying within a step budget. Don't require one exact sequence of steps, because agents often find another route that is just as good.*

*"How it's checked" has three options. Use code when there is a right answer a script can test. Use an AI judge for things like tone or whether a claim is backed by the source, and check it against your own labels first. Use a person for anything new, rare or high stakes. [Choosing Graders](../toolkit/choosing-graders.md) goes deeper.*

## 8. Is the AI worth it?

*Most of this can only be measured once real users have it. Agree the numbers now so engineers log what's needed from day one.*

- **The business metric it should move:** *for example tickets avoided, time saved or tasks completed, and the size of change that would count as success*
- **What it may cost:** *cost per task or per user that the business can live with*
- **How fast it must be:** *response time users will accept*

## 9. Watching it in production

*This tells engineers what to log and which monitors to build. Fill in one row for each question.*

| Question | What we watch | What engineers log and build |
|---|---|---|
| Right | *A weekly sample of whole conversations scored by the same checks as section 7; thumbs-down; users asking again, rephrasing, or opening a ticket soon after* | *Every input, output and source used; user feedback; a review queue for sampled conversations* |
| Safe | *The section 3 rules checked on live traffic* | *Which documents and tools each answer used; alerts that fire on any broken rule; a way to switch the feature off quickly* |
| Worth it | *The business metric, cost and response time from section 8* | *Outcome events joined to conversations; cost and response time per request; a dashboard* |

- **Who reads real conversations, and how often:** *a good default is the PM and a domain expert, weekly*
- **What happens to new failures:** *each one becomes a new example case, so it's tested on every release*

---

## For engineers: what to build from this document

| Section | What it becomes |
|---|---|
| 2. Is the AI right? | One check per item: a code check where possible, otherwise a yes/no AI judge ([judge template](judge-prompt.md)) |
| 3. Is the AI safe? | Blocking checks that run on every release, ideally in CI |
| 5. Example cases | The first test set, one case per row. Conversations become cases with a checkpoint at each turn, run several times each ([case format](golden-case.schema.json)) |
| 6. Known ways it fails | Extra cases aimed at each failure, kept as regression tests |
| 7. Definition of done | Pass bars in [`eval-prd.yaml`](eval-prd.yaml). [`run_code_graders.py`](../scripts/run_code_graders.py) shows how a failed bar stops a release. |
| 8 and 9. Worth it and production | Logging, monitors, alerts, dashboards and a review queue for real conversations |

If the feature matches one of the [use-case packs](../README.md#go-deeper), its failure modes and test data mix are a good source of extra cases.
