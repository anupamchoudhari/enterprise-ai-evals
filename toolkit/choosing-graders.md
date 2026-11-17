# Choosing Graders

*Used in the **Measure** stage of [the Loop](../framework/the-loop.md).*

A grader is whatever decides whether an output passes a check. There are three kinds. In order of preference: **code**, **LLM judge**, **human**. Use the cheapest one that can reliably catch the failure.

## Which grader to use

```
Is there an objective right answer, or a property you can check mechanically?
 ├─ Yes ─► CODE CHECK
 │         (exact match, regex, JSON schema, SQL execution,
 │          document ID lists, tool-call assertions, before/after state)
 └─ No ──► Could an expert decide pass or fail from the output alone,
           using a one-sentence rule?
            ├─ Yes ─► LLM JUDGE (one yes/no rule per judge),
            │         checked against human labels before you trust it
            └─ No ──► HUMAN REVIEW, and keep labeling until you can
                      write the rule down
```

Code checks that PMs often overlook:

- **Forbidden document check:** did any retrieved or cited document appear on this user's forbidden list?
- **Before/after state:** compare the system before and after an agent run (records created, emails sent, money moved).
- **Numbers check:** every number in the answer appears in the source.
- **Format check:** valid schema, length limit, required sections present.

## Writing a judge

1. **One rule per judge**, with a PASS or FAIL verdict and a short reason.
2. **Give it the evidence it needs:** the request, the sources, a reference answer if you have one, and the relevant policy.
3. **Show it examples of FAIL** from your discovery work, including borderline cases in both directions.
4. **Ask for its reasoning before the verdict.**
5. **Use a judge from a different model family** than the model being evaluated, where you can. Judges tend to favor text from their own family.
6. **For A-versus-B comparisons, run both orders** and count it as a tie when the verdict flips with the order.

Template: [`templates/judge-prompt.md`](../templates/judge-prompt.md).

## Checking a judge against humans

An LLM judge is a model with its own blind spots, so measure it before relying on it. Have a domain expert label at least 100 outputs that the judge hasn't seen in its examples, with enough failures among them to measure how many the judge catches. Then compare.

| Measure | Plain meaning | Why it matters | Technical name |
|---|---|---|---|
| **Failures caught** | Of the outputs the expert failed, how many did the judge also fail? | If this is low, bad outputs ship without anyone noticing | True positive rate (TPR), recall on FAIL |
| **Good outputs passed** | Of the outputs the expert passed, how many did the judge also pass? | If this is low, the team drowns in false alarms and stops trusting the judge | True negative rate (TNR) |

Suggested minimums by [stakes](../framework/the-stakes.md):

| Stakes | Failures caught | Good outputs passed |
|---|---|---|
| Low | 80% | 80% |
| Medium | 90% | 85% |
| High | 95%, plus human spot checks of what the judge passes | 85% |

Check the judge again whenever the judge model, its prompt or the style of the product's outputs changes. Known judge biases (favoring the first option, longer answers, Markdown formatting, or its own model family) shift between model versions, so measure them on your own data.

## Correcting a reported pass rate

A judge that misses some failures and flags some good outputs reports a pass rate that is off from the truth. If the judge reports a pass rate `p`, a better estimate of the true pass rate is:

```
true pass rate ≈ (p + TPR - 1) / (TPR + TNR - 1)
```

Use the corrected number when you report results to leadership, along with a confidence interval from your labeled set. If TPR + TNR is close to 1, the judge is no better than a coin flip.
