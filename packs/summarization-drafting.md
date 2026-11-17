# Pack: Summarization and Drafting

**Applies to:** meeting and call summaries, ticket/case summaries, document briefs, email and message drafting, report generation, job description or policy drafting.
**Typical stakes:** Low when a person edits before sending; Medium when the output is sent or stored as a record with little review.

## Failure modes
`unsupported-claim` (invented names, numbers, dates or action items) · leaving out the one thing that mattered · misattribution (who said or agreed to what) · `wrong-tone` · `too-long` · `broken-format` · leftover template text · `personal-data-exposed` (sensitive details that should have been left out)

## Metrics

| Question | Metric | Grader | How |
|---|---|---|---|
| Right | Factual consistency | Judge + code | Every claim supported by the source; numbers and named entities appear in the source (code) |
| Right | **Key-point coverage** | Judge | Covers a reference list of must-include points written by an expert per source |
| Right | Attribution accuracy | Judge | Statements and decisions attributed to the right person |
| Right | Action item accuracy | Code + judge | Precision and recall vs reference action items (owner + due date) |
| Right | Format contract | Code | Required sections present, length within limit |
| Safe | Sensitive-content filter | Judge | Omits content that should not travel (HR complaints in a team summary, health details) |
| Worth it | **Edit distance to sent version** | Analytics | How much users change the draft before sending. A falling edit rate is one of the most useful online signals for drafting. |
| Worth it | Acceptance rate | Analytics | Share of drafts used at all |

## Dataset design
- 50 to 150 real source documents per summary type, each with an expert-written must-include list (5 to 10 bullets) and a must-not-include list.
- Include long sources (to catch "lost in the middle"), sources with numbers and dates, sources where the key point is stated once and late, and sources with conflicting statements.
- For drafting, pair the request with the intended audience and relationship (manager to report, vendor to customer) since tone correctness depends on it.

## Pass bars (Low and Medium stakes default)
- Fabricated entity or number rate: 0 on golden set
- Key-point coverage >= 90%
- Attribution accuracy >= 95% for meeting summaries
- Online: edit distance trending down; acceptance trending up

## Tip
Pairwise comparison ("is A or B the better summary?") is useful for choosing between prompt versions, but swap positions and control for length, since judges are known to be swayed by order and verbosity.
