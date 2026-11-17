# Pack: Security and Red Teaming

**Applies to:** every LLM feature that reads untrusted input (user text, documents, emails, web pages, tool outputs) or can take actions. In practice: all of them.
**Typical stakes:** the same as the feature being tested. Adversarial testing is required from Medium upward.

Use the OWASP lists as the coverage checklist: the [Top 10 for LLM Applications 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/) (prompt injection and sensitive information disclosure remain #1 and #2) and, for anything with tools or memory, the [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (goal hijacking, tool misuse, privilege abuse, memory poisoning, rogue agents).

## Attack families and what to measure

| Family | Test | Metric | Grader |
|---|---|---|---|
| Direct prompt injection | User tries to override instructions, extract system prompt, change persona | Attack success rate (ASR) | Code (canary strings) + judge |
| **Indirect prompt injection** | Instructions hidden in retrieved docs, emails, tickets, web pages, tool outputs, file names | ASR; unauthorized tool calls triggered | Code (state diff, tool-call log) |
| Data exfiltration | Get the model to put sensitive data into a URL, image link, email or tool argument | Exfil attempts executed | Code |
| Sensitive info disclosure | Ask for other users' data, secrets, internal config | Leak rate | Code (canaries) |
| Hidden context exposure | Extract system prompt or tool descriptions | Exposure rate | Code (canary in system prompt) |
| Tool misuse / privilege abuse | Coax the agent into out-of-scope or destructive calls | Out-of-scope call rate | Code |
| Memory poisoning | Plant a false "fact" or instruction in memory that alters later sessions | Persisted malicious memory rate | Code + judge |
| Unbounded consumption | Prompts that cause runaway loops or huge outputs | Max cost/tokens per request | Telemetry |
| Jailbreak to policy-violating content | Domain-relevant harmful asks | Violation rate | Judge |

**Canary technique:** put unique random strings in the system prompt, in restricted documents and in other tenants' data. Any appearance in output or tool arguments is a detected leak, gradable by string match with no judge needed.

## Process
1. Build a seed set from OWASP categories mapped to *your* tools and data.
2. Expand automatically (Promptfoo and DeepTeam can generate attack variants) and with a human red team before major launches.
3. Run the full adversarial suite on every change to prompts, tools, retrieval sources or models.
4. Report ASR for each attack family separately. A single blended "safety score" hides which defense failed.

## Pass bars
- Medium stakes: ASR on indirect injection leading to an action: 0; canary leaks: 0; other families tracked with downward trend
- High stakes: the above plus an independent red-team exercise and a documented incident runbook

## Remember
Security comes from the controls themselves: ACLs in retrieval, tool allowlists, confirmation steps and output filtering. The evals in this pack are there to prove those controls keep holding, release after release.
