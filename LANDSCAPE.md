# The AI Evals Landscape (as of November 2026)

This is a map of what already exists, so the repo can build on it instead of repeating it. Entries are grouped by how a PM would use them. Each one links to a primary or reputable source. The space changes month to month, so check current versions before you adopt anything.

---

## 1. Methodology: how good teams build evals

| Source | What to take from it |
|---|---|
| Hamel Husain & Shreya Shankar, [AI Evals FAQ](https://hamel.dev/blog/posts/evals-faq/) and [Building eval systems that improve your AI product](https://www.lennysnewsletter.com/p/building-eval-systems-that-improve) | Start from real traces and read them before choosing any metric. Error analysis produces a prioritized list of failure modes, and automated evaluators are built for those. In many products the PM is the principal domain expert and should be doing the labeling. |
| Husain & Shankar, [Advanced evals: How to find (and fix) hidden AI failures](https://lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix) (Sep 2026) | They now call the first step **error discovery**, because the aim is to find the failures worth measuring, much like product discovery finds the problems worth solving. |
| Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Jan 2026) | A shared vocabulary for agent evals (task, trial, grader, transcript, outcome, harness) and three grader types: code, model and human. It separates **capability evals**, which ask whether the agent can do something at all, from **regression evals**, which ask whether it still does it reliably. It also makes the case that evals are the main channel between product and research teams. |
| Teresa Torres, [AI Evals: A Hands-On Guide for Product Teams](https://www.producttalk.org/ai-evals/) | How much error analysis you do should depend on what a bad output costs. |
| Product Compass, [How to find the right AI product metrics](https://www.productcompass.pm/i/165394671/how-to-turn-failure-modes-into-app-specific-ai-metrics) | Generic metrics such as "hallucination" or "toxicity" tend to miss domain-specific problems. Let app-specific metrics come out of your own data, and measure the evaluators themselves with TPR and TNR. |
| Aakash Gupta, [The PM's role in AI evals](https://www.news.aakashg.com/p/hamel-shreya-podcast) | If offline evals improve while user metrics stay flat, go back to error analysis. |
| Braintrust, [Evals are the new PRD](https://www.braintrust.dev/blog/evals-are-the-new-prd); also [Mind the Product](https://www.mindtheproduct.com/evals-are-the-new-prd/) and [The New Stack on Anthropic](https://thenewstack.io/anthropic-evals-replace-prds/) | For AI features, the eval set is the most precise statement of what the product should do. This repo turns that argument into a template a PM fills in. |

**What this adds up to:** the method has largely converged. Teams review traces, find failure modes, build targeted evaluators, calibrate their LLM judges, gate releases in CI and keep monitoring in production. What is still thin is guidance on *what* to measure for a given enterprise use case and which thresholds to ship on.

Most of this guidance also assumes you already have production traces. A team shipping its first agent usually doesn't. Their best source of failure modes is the workflow the agent is replacing, which [Discovery Before Launch](toolkit/discovery-before-launch.md) covers.

### Multi-turn conversations and non-determinism

Most eval sets are single questions graded on a single run. The research says that's where AI looks best:

- **Models get lost across turns.** [LLMs Get Lost in Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) (Laban et al., Microsoft and Salesforce, 2025) gave 15 models the same tasks as one message and spread over several turns. Performance dropped by about 39% on average, mostly because answers became unreliable. Models commit to an early guess and don't recover when the user adds detail.
- **Enterprise agents do worse over several turns.** In [CRMArena-Pro](https://arxiv.org/abs/2505.18878), leading agents scored about 58% on single-turn tasks and about 35% on multi-turn ones.
- **One good run proves little.** [τ-bench](https://github.com/sierra-research/tau-bench) introduced pass^k, the chance an agent succeeds on all k tries, because pass rates fall sharply as k grows.
- **Grade the session, then find the first failure.** Husain and Shankar recommend grading a whole conversation pass or fail, then finding the first turn that went wrong and reproducing it as a smaller test where possible.
- **Grade outcomes and a few path rules.** Anthropic's agent guidance warns against requiring one exact sequence of steps, since agents often find valid routes the eval author didn't anticipate. Check the end state, plus rules that must hold on any path.

The Eval PRD applies this with conversation cases that have a checkpoint at each turn, a judge for the whole conversation, and pass bars that count a case only when every repeated run passes.

## 2. Open-source eval libraries and harnesses

| Tool | Best for |
|---|---|
| [DeepEval](https://deepeval.com) (Confident AI) | Pytest-style test cases, metrics and thresholds that run locally and in CI |
| [Ragas](https://docs.ragas.io) | RAG metrics (faithfulness, answer relevancy, context precision and recall) and synthetic test data |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | YAML-driven prompt and model comparison, plus red teaming. Reported to be under acquisition by OpenAI, with the open-source project continuing. |
| [Inspect](https://inspect.aisi.org.uk) (UK AI Security Institute and Meridian Labs) | Reproducible agentic and multi-turn evals with sandboxing. METR and Apollo Research both run on it. |
| [MLflow Evaluate](https://mlflow.org) | Tracing, scoring and judge optimization in one self-hostable tool |

## 3. Eval and observability platforms

This segment is crowded. There are many commercial vendors and a good number of open-source options, and new entrants appear every quarter. Commonly evaluated ones include MLflow, LangSmith, Braintrust, Confident AI, Langfuse, Arize Phoenix, Opik, W&B Weave and Galileo. [MLflow](https://mlflow.org/articles/tags/rag-evaluation-tools/) and [FutureAGI](https://futureagi.com/blog/best-llm-evaluation-tools-2026/) have both published comparisons; keep in mind that both are vendors in the category.

**PM lens.** Choose for the review workflow first and the feature list second.

- **Non-engineers need access to traces, with the right permissions and context.** Domain experts, support leads or HR specialists often do the most valuable labeling. Look for a tool that lets you build **annotation queues** scoped to a reviewer's role, shows the context they need to judge an output (the user's question, the retrieved sources, the tools called), and keeps them out of data they shouldn't see.
- **Plan for a redaction layer.** Traces from enterprise products contain PII. Redacting it before review is a privacy requirement. In some applications it also reduces labeling bias: in hiring or performance use cases, a reviewer who can see a candidate's name, gender or age can be swayed by it, so those fields should be masked during review.
- **The same scorers should run offline and on live traffic**, so a failure found in production turns into a regression test without rework.

## 4. Benchmarks that resemble enterprise work

| Benchmark | What it tests | Why a PM should care |
|---|---|---|
| [τ-bench / τ²-bench](https://github.com/sierra-research/tau-bench) (Sierra) | An agent talks to a simulated user, calls APIs and follows a policy manual across retail, airline, telecom and banking | Introduced **pass^k** (the agent succeeds on all k trials), which is the right reliability measure for production agents |
| [CRMArena-Pro](https://arxiv.org/abs/2505.18878) (Salesforce) | 19 expert-validated CRM tasks across sales, service and CPQ, plus confidentiality awareness | Leading agents scored about 58% single-turn and about 35% multi-turn, which shows how far generic agents are from enterprise needs |
| [Spider 2.0](https://arxiv.org/abs/2411.07763) and BIRD | Text-to-SQL on enterprise-scale schemas and dialects such as BigQuery and Snowflake | About 91% on Spider 1.0 dropped to about 21% on Spider 2.0 at release. Accuracy on small, clean schemas does not carry over to real warehouses. |
| [LongMemEval](https://github.com/xiaowu0162/LongMemEval) and [LongMemEval-V2](https://xiaowu0162.github.io/longmemeval-v2/) | Long-term memory: extraction, multi-session reasoning, temporal reasoning, knowledge updates and abstention. V2 adds workflow knowledge and environment "gotchas" for agents. | A good template for evaluating memory and personalization layers |
| WorkArena, SWE-bench, OSWorld, GAIA | Knowledge-work UI tasks, coding, computer use, research | Their task design is worth borrowing. Their scores tell you little about your product. |
| [DevRev Enterprise AI Agent Benchmark](https://thenewstack.io/enterprise-ai-benchmarks-are-broken/) (Jul 2026) | Agents working over messy enterprise data at scale, with traces released | Open harness and judging criteria you can study |
| [CLEAR framework](https://arxiv.org/abs/2511.14136) | Cost, Latency, Efficacy, Assurance, Reliability for enterprise agents | A useful shape for a multi-dimensional scorecard |

As a rule of thumb, treat public benchmark scores as one input when choosing a model. Don't use them to decide whether your feature is ready to ship. In April 2026 an automated agent reportedly reached near-perfect scores on several leading agent benchmarks by [exploiting flaws in the harness](https://www.automationanywhere.com/company/blog/ai-agent-benchmarks) without solving the tasks.

## 5. Security, safety and governance frameworks

| Framework | Use it to |
|---|---|
| [OWASP Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (Aug 2026) | Seed adversarial eval cases. Prompt injection and sensitive information disclosure remain #1 and #2. |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (Dec 2025) | Cover agent-specific risks: goal hijacking, tool misuse, privilege abuse, memory poisoning and rogue agents |
| NIST AI RMF, ISO/IEC 42001 | Map your evals to the controls your security and compliance teams already track |
| EU AI Act | AI used in employment, credit, education and similar areas is classed as high-risk. After the Digital Omnibus, [standalone Annex III high-risk obligations apply from 2 Dec 2027](https://www.holisticai.com/blog/eu-ai-acts-deadline-moved-2027), and obligations for general-purpose models already apply. Testing evidence is part of compliance, so your eval logs double as audit records. |

## 6. Research on LLM-as-judge reliability

An LLM judge is itself a model with measurable biases, so its verdicts need checking like any other model output. The documented biases include:

- **Position bias:** in pairwise comparisons, the answer shown first (or second) wins more often than it should ([Zheng et al.](https://arxiv.org/abs/2306.05685))
- **Verbosity bias:** longer answers get higher scores even when the extra length adds nothing
- **Self-preference:** judges favor text from their own model family ([Panickssery et al.](https://arxiv.org/abs/2410.21819))
- **Style and format bias:** [a 2026 study](https://arxiv.org/abs/2604.23178) found a strong preference for Markdown-formatted answers, larger than the position effect

Practical mitigations:

- Use binary, criteria-based rubrics
- In pairwise comparisons, run both orderings
- Avoid using a model to judge outputs from its own family
- Recalibrate against a human-labeled set whenever the judge model or prompt changes

## 7. Curated lists worth following

- **[benchflow-ai/awesome-evals](https://github.com/benchflow-ai/awesome-evals)**: the strongest of the lists. It is focused on agent evaluation, opinionated about what is worth reading, actively maintained, and it flags links it hasn't verified. Start here.
- [Awesome-LLM-Eval](https://github.com/onejune2018/Awesome-LLM-Eval): broad coverage of benchmarks, leaderboards and papers, leaning toward model-level evaluation
- [awesome-ai-eval](https://github.com/Vvkmnn/awesome-ai-eval): tools and platforms for evaluating AI in applications
- [awesome-llm-judges](https://github.com/haizelabs/awesome-llm-judges): research on LLM judges

---

## 8. Where this repo fits

1. **Existing repos mostly catalog resources.** They list tools, papers and benchmarks. Very few give a PM a spec to fill in for a specific enterprise use case.
2. **Golden sets rarely test permissions or tenancy.** Most RAG eval sets list the documents that should be retrieved and leave out the ones that must never be. Without that second list they cannot catch cross-role or cross-tenant leakage, which is the [failure found most often](https://www.bdemerson.com/article/rag-security) in enterprise RAG assessments.
3. **NL2SQL evals skip the semantic layer.** Execution accuracy on public schemas tells you nothing about whether "active employee" or "net revenue" matches *your* metric definitions.
4. **Agents that change state get little coverage.** Benchmarks grade task completion. Enterprise SaaS also needs evals for confirming before irreversible actions, idempotency and least-privilege tool use.
5. **Offline scores are rarely connected to business metrics,** or to pass bars that change with the stakes.
6. **First launches get little guidance.** Teams without production traces need a way to discover failure modes from the workflow they are automating.
7. **Conversations are graded one reply at a time.** Most golden sets are single questions run once, which misses the failures that happen on the third turn or on one run in five.
8. **Memory and personalization** in enterprise settings (stale facts, one user's context leaking into another's, the right to be forgotten) has little coverage outside research benchmarks.

---

*A note on licensing: everything in sections 2 and 3 described as open source has a publicly available codebase. License terms vary, and a few projects are source-available or keep some features commercial, so check the license file in each repository before using it in a commercial product.*
