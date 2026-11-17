# Contributing

Thanks for helping make AI evals more practical for product teams.

## What is most useful
- **Failure modes from production** (anonymized): what broke, how you detected it, and what evaluator now catches it.
- **Gates that held up:** thresholds you shipped on, and whether they predicted production quality.
- **New packs or domain overlays**, following the existing pack structure.
- **Corrections:** outdated tool details, broken links, wrong attributions.

## Guidelines
1. Keep it tool-agnostic. Mention tools as options that readers can swap for their own.
2. Cite sources for factual claims about tools, benchmarks and regulations, with links to primary sources where possible.
3. No proprietary or customer data. Examples must be synthetic or fully anonymized.
4. Prefer binary, observable criteria over 1-to-5 scales.
5. Plain language. Write for a PM reading on a phone between meetings.

## Pack structure
Every pack should include: applies to and typical stakes, failure modes (using the failure tags), a metrics table (risk, metric, grader, how), test data design, pass bars, production signals, and what to borrow.

## Process
Open an issue to discuss larger changes, then send a pull request. Run `python scripts/run_code_graders.py` on the example if you touch the templates or script.
