# The Loop

Four stages that most product teams already know: **Define, Discover, Measure, Monitor**. Run them in order the first time, then keep cycling. Each pass through Monitor feeds new failures back into Discover.

```
 Define ──► Discover ──► Measure ──► Monitor
              ▲                         │
              └──── new failures ───────┘
```

## 1. Define

**Question:** What job is the AI doing, for whom, and what happens when it gets it wrong?

- Start the [Eval PRD](../templates/eval-prd.md): the job, what good looks like, and what must never happen.
- Decide the [stakes](the-stakes.md): Low, Medium or High.
- **Owner:** PM. Bring in engineering, and security or legal when the stakes are High.
- **Done when:** sections 1 to 4 of the Eval PRD are filled in and the stakes level is agreed.

## 2. Discover

**Question:** How does it actually fail?

- **If you have traces** (from production, a beta or dogfooding): review 50 to 200 of them. Write a short note on what went wrong in each, then group the notes into failure modes using the [failure tags](../toolkit/failure-tags.md). Rank them by how often they happen and how bad they are.
- **If you don't have traces yet** (first launch): use [Discovery Before Launch](../toolkit/discovery-before-launch.md). The workflow the AI is replacing has years of recorded failures in tickets, audits and escalations.
- **Owner:** PM with a domain expert. In many products the PM is the domain expert.
- **Done when:** the last 20 or so traces you reviewed turned up no new failure mode.

## 3. Measure

**Question:** Can we detect each failure automatically, and is the feature good enough to ship?

1. **Build checks.** Give each important failure mode its own check, and group them under the [three questions](the-three-questions.md). Use the cheapest grader that works: a code check first, an LLM judge second, human review third ([Choosing Graders](../toolkit/choosing-graders.md)).
2. **Calibrate the judges.** Compare every LLM judge with human labels before trusting its scores.
3. **Set the bar and gate releases.** Take the default pass bars for your stakes level, write them into the spec, and run them in CI on every change.

- **Owner:** engineering builds the checks; the PM labels the calibration data and owns the pass bars.
- **Done when:** every top failure mode has a check, every judge is calibrated, and the pass bars run automatically in CI.

## 4. Monitor

**Question:** Is it still working in production, and is it moving the business metric?

- Run the same checks on a sample of live traffic.
- Review traces every week. Thirty to sixty minutes per product surface is usually enough.
- Track the "worth it" metrics (adoption, task completion, deflection, time saved, cost per task).
- Turn every production incident into a regression test within a sprint.
- **Owner:** PM and engineering together.
- This stage keeps running for the life of the feature. Anything new goes back to Discover.

## Working principles

1. **Read real outputs before choosing metrics.** Metric libraries are a useful vocabulary. Your checks should come from the failures you actually found.
2. **Prefer yes/no checks.** "Did the answer cite a document this user can't access?" is easier to label, calibrate and act on than a 1 to 5 safety rating.
3. **Give each failure mode its own check.** A blended quality score hides which thing broke.
4. **Keep two suites.** A capability suite tracks what you are still building, and it's fine for it to score low. A regression suite protects what already works and should stay near 100%. Move cases from the first to the second once they pass reliably.
5. **Test conversations, and run them more than once.** Many failures only show up on turn 3 or later, and the same case can pass on one run and fail on the next. Check each turn and the whole conversation, and report pass^k (the case passes on all k runs) alongside the single-run pass rate.
6. **Treat the eval set as a product asset.** Version it, review changes to it, and give it an owner.

## Cadence

| When | What |
|---|---|
| Every change to prompts, retrieval, tools or models | Regression suite in CI |
| Weekly | Trace review and tagging of new failures |
| Every release | Full suite including capability and adversarial cases, plus an [eval report](../templates/eval-report.md) |
| Model or judge change | Treat it as a migration: rerun calibration and compare each failure mode before switching |
| Quarterly | Refresh the golden set from recent traffic and retire stale cases |
