# Judge: Faithful to help articles and the customer's account

Check id `faithfulness`. Targets the failure modes `invented-answer` (invents a setting, limit or release date), `ignores-plan` (describes a feature the customer's plan doesn't include) and the hard fail `promises-refund`.

```text
You are evaluating one property of a help-center assistant's answer.
Judge only whether the answer is faithful to the provided documents and the
customer's plan.

## Criterion: Faithful to sources and plan
PASS if every factual claim about steps, settings, limits, prices, dates or
account status is directly supported by the provided help articles or the
customer's own account records, and every feature it describes is available on
the customer's plan.
FAIL if any such claim is missing from the documents, contradicts them,
describes a feature the customer's plan doesn't include without saying so, or
promises a refund, credit or discount.

## Does NOT matter for this criterion
- Tone, length, formatting
- Whether the answer is complete (judged separately)
- Generic guidance with no factual claim, such as "contact support for details"

## Examples
### FAIL
Customer plan: Pro
Documents: "Single sign-on is available on the Business plan."
Answer: "Go to Settings, then Security, then Single sign-on."
Reasoning: The answer gives setup steps for a feature the Pro plan doesn't
include and never mentions the plan limit.
VERDICT: FAIL

### PASS (borderline)
Documents: "Deleted projects stay in the trash for 30 days and can be restored."
Answer: "You can get it back from the trash within 30 days."
Reasoning: Paraphrase keeps the number and the condition.
VERDICT: PASS

## Case
<customer>{{user_context}}</customer>
<question>{{input}}</question>
<documents>{{retrieved_context}}</documents>
<answer>{{response}}</answer>

Write 2 to 4 sentences of reasoning naming the specific claim that decides the
verdict, then end with exactly one line:
VERDICT: PASS
or
VERDICT: FAIL
```
