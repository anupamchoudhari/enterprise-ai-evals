# Pack: Extraction, Classification and Routing

**Applies to:** document parsing (invoices, contracts, resumes, benefit forms, IDs), ticket triage and routing, intent detection, tagging, entity resolution, structured output from unstructured input.
**Typical stakes:** Low to Medium; High when extracted values drive payments or eligibility decisions without review.

This is the most "classical ML" pack: there is usually a right answer, so code graders do most of the work. Do not reach for an LLM judge here unless the field is genuinely subjective.

## Failure modes
Wrong value · missing field · invented field · wrong format, units or currency · wrong label on look-alike classes · confident output on unreadable input · `broken-format`

## Metrics

| Metric | Grader | Notes |
|---|---|---|
| Field-level precision, recall, F1 | Code | Report per field as well as overall. A 98% average can hide a 70% field that matters most. |
| Exact match after normalization | Code | Normalize dates, currency, whitespace, case before comparing |
| Schema validity | Code | 100% expected |
| Classification accuracy, macro-F1 | Code | Macro-F1 so rare classes count |
| Confusion matrix on critical pairs | Code | E.g. "billing dispute" vs "billing question" |
| **Abstention quality** | Code | Returns null/low confidence on illegible or missing fields instead of guessing |
| Confidence calibration | Code | When the system says 90% confident, is it right about 90% of the time? Needed if you auto-route above a threshold. |
| Routing cost-weighted error | Code | Weight misroutes by downstream cost (misrouted P1 incident costs more than misrouted FAQ) |

## Dataset design
- Stratify by document source and quality: clean digital, scanned, photographed, multi-page, non-English, handwritten fields.
- Hold out a set of **templates the system has never seen** to measure generalization.
- For routing: sample real tickets proportionally, then oversample rare but costly classes.

## Pass bars (Medium stakes default)
- Critical fields (amounts, IDs, dates): precision >= 99%, recall >= 97%
- Schema validity 100%
- At the chosen auto-accept confidence threshold, error rate below the human baseline you are replacing

## Tip
Measure the human baseline. Teams often hold AI to a 99% bar that the current manual process does not meet. The right gate is usually "better than today at equal or lower cost", with the review queue absorbing low-confidence cases.
