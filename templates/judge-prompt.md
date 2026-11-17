# Judge Prompt Template (binary, single criterion)

Copy and fill in the bracketed parts. One judge per failure mode. Calibrate against human labels before trusting it (toolkit/choosing-graders.md).

```text
You are evaluating one specific property of an AI assistant's response.
You are not rating overall quality. Judge only the criterion below.

## Criterion: [SHORT NAME, e.g. "Faithful to sources"]
PASS if: [precise, observable condition]
FAIL if: [precise, observable condition]

## What does NOT matter for this criterion
- Length, formatting, tone, or writing style
- [Other properties evaluated by separate judges]

## Examples
### Example 1 (FAIL)
Input: [...]
Response: [...]
Reasoning: [why it fails, one or two sentences]
Verdict: FAIL

### Example 2 (PASS)
[...]

### Example 3 (borderline, PASS)
[A case that looks like a failure but is not, with reasoning]

## Case to evaluate
<user_request>
{{input}}
</user_request>

<context>
{{retrieved_context_or_policy}}
</context>

<reference>
{{reference_answer_or_required_facts_if_any}}
</reference>

<response>
{{output}}
</response>

First write your reasoning in 2 to 4 sentences, citing the specific part of
the response that drives your decision. Then output the verdict on the last
line as exactly one of:
VERDICT: PASS
VERDICT: FAIL
```

## Checklist before use
- [ ] Criterion is binary and could be applied consistently by two different experts
- [ ] Examples come from real traces found during error discovery
- [ ] At least one borderline example in each direction
- [ ] Judge model is from a different family than the model being evaluated, where practical
- [ ] Calibrated: TPR and TNR measured on 100+ human-labeled cases held out from the examples
- [ ] Judge prompt and judge model version are pinned and recorded in eval results
