# Pack: People Decisions and Other High-Risk Uses (HR, Compensation, Benefits, Credit)

**Applies to:** resume screening and candidate ranking, interview summaries, performance review assistance, compensation recommendations, benefits eligibility, promotion or attrition prediction, credit or insurance decisions.
**Typical stakes:** High.

Employment and credit uses are high-risk under the EU AI Act (Annex III); after the Digital Omnibus, [standalone high-risk obligations apply from 2 December 2027](https://www.holisticai.com/blog/eu-ai-acts-deadline-moved-2027). Many US jurisdictions also regulate automated employment decision tools. Evals here double as compliance evidence, so keep them versioned and reproducible. This pack is not legal advice; involve counsel to set the actual requirements.

## Failure modes
`uneven-quality` across groups · `protected-attribute-used` (directly or through a proxy) · `unsupported-claim` (invented qualifications or performance claims) · different decisions on equivalent inputs · no human review of adverse outcomes · an explanation that doesn't match the actual basis of the decision · `personal-data-exposed`

## Metrics

| Metric | Grader | How |
|---|---|---|
| **Counterfactual consistency** | Code | Swap names, pronouns, ages, schools, gaps or addresses (proxies) on otherwise identical inputs; outcome and score must not change beyond tolerance |
| Group outcome rates | Code | Selection/approval rates by group; compare ratios (e.g. the four-fifths rule used in US employment practice) where you have lawful demographic data |
| Group error rates | Code | False positive/negative rates by group against expert labels |
| Decision consistency | Code | Same input across k runs gives the same decision (pass^k on the decision) |
| Explanation faithfulness | Judge + human | Stated reasons are actually present in the input and match the criteria used |
| Criteria adherence | Judge | Uses only job-relevant or policy-defined criteria |
| Human review coverage | Code | 100% of adverse or borderline outcomes routed to a person |
| Factual accuracy of summaries | Judge | No invented skills, ratings or quotes |

## Dataset design
- Expert-labeled cases from historical decisions, reviewed for historical bias before being used as ground truth (past decisions can encode the bias you are testing for).
- **Counterfactual pairs** generated systematically: for each base case, variants differing only in one protected attribute or proxy.
- Edge cases: career gaps, non-traditional education, international credentials, part-time history, accommodations.
- **Redact before human review.** Mask names, photos, ages, addresses and other identity signals in the annotation tool, so labelers judge the output on job-relevant criteria. This protects privacy and keeps reviewer bias out of your ground truth.

## Pass bars (High stakes default)
- Counterfactual flips: 0 on decision; score deltas within a tolerance agreed with legal
- No group with materially worse error rates without a documented, approved justification
- Decision consistency pass^8 >= 99%
- Human review on 100% of adverse outcomes
- Independent review (not the building team) of the eval design before launch

## Keep for audit
Eval spec, dataset versions, judge prompts and calibration, results per release, and sign-offs. Treat them as records.
