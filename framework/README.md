# The Framework: Loop, Questions, Stakes

> **Run the Loop. Ask if the AI is right, safe and worth it. Set the bar by the stakes.**

The framework has three parts, and each one answers a different question.

| Part | Question it answers | In short |
|---|---|---|
| [**The Loop**](the-loop.md) | How do we work? | **Define, Discover, Measure, Monitor**, repeated for the life of the feature |
| [**The Three Questions**](the-three-questions.md) | What do we evaluate? | **Is the AI right? Is the AI safe? Is the AI worth it?** A plain-language regrouping of Marty Cagan's four big product risks |
| [**The Stakes**](the-stakes.md) | How strict do we need to be? | **Low, Medium or High**, decided by who relies on the output and what a mistake costs |

```
            ┌──────────── The Loop ────────────┐
            │                                  │
   Define ──► Discover ──► Measure ──► Monitor ─┘
     │                        │
     │ sets the Stakes        │ asks the Three Questions
     ▼                        ▼
 Low / Medium / High     Right · Safe · Worth it
 (how high the bar is)   (what gets measured)
```

**How the parts fit together.** In **Define** you decide the stakes. In **Discover** you find out how the feature actually fails. In **Measure** you build checks for those failures, grouped under the three questions, and the stakes decide the pass bar for each one. In **Monitor** you watch production, and anything new goes back to Discover.

## Toolkit

These are the working tools you use inside the Loop. A PM starting out only needs the Eval PRD.

| Tool | Used in | What it is for |
|---|---|---|
| [Eval PRD](../templates/eval-prd.md) | All four stages | The one document a PM writes: what good looks like, example cases, the definition of done and what to watch after launch |
| [Discovery Before Launch](../toolkit/discovery-before-launch.md) | Discover | Finding failure modes when you have no production traces yet |
| [Failure Tags](../toolkit/failure-tags.md) | Discover | A shared vocabulary for tagging what went wrong |
| [Choosing Graders](../toolkit/choosing-graders.md) | Measure | Picking between code checks, LLM judges and human review, and calibrating judges |

## Where the ideas come from

Most of this framework assembles and adapts existing practice. The table shows what is borrowed and what is new.

| Part | Built on | What this repo adds |
|---|---|---|
| The Loop | The error analysis loop taught by Hamel Husain and Shreya Shankar ([evals FAQ](https://hamel.dev/blog/posts/evals-faq/), [Lenny's Newsletter](https://www.lennysnewsletter.com/p/building-eval-systems-that-improve)); Anthropic's split between capability and regression evals ([Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)) | Four stages named in familiar product language, with owners, outputs and exit checks |
| The Three Questions | Marty Cagan's [four big risks](https://svpg.com/product-risk-taxonomies) (value, usability, feasibility, viability) from SVPG and *INSPIRED* | Cagan uses the risks in product discovery, before anything is built. Here they are reused to organize evals and regrouped into three questions: right (usability and feasibility), safe (the safety side of viability) and worth it (value, plus cost). |
| The Stakes | The risk-based approach of the EU AI Act and NIST AI RMF | Three plain-language levels, three questions to pick one, and default pass bars per level |
| Choosing Graders | Anthropic's three grader types; Husain and Shankar on checking judges against human labels | A decision tree and suggested agreement bars by stakes level |
| Discovery Before Launch | Shadow mode, dogfooding and Gary Klein's pre-mortem | Applied to first-time agent launches, with the current workflow as the source of failures |
| Failure Tags | Open coding from qualitative research, popularized for evals by Husain and Shankar; the OWASP Top 10 lists for LLM and agentic applications | A starter tag set for enterprise SaaS, with each tag mapped to one of the three questions |
