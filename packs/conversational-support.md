# Pack: Conversational Support and In-Product Copilots

**Applies to:** customer support bots, employee helpdesks (IT, HR, benefits), in-app assistants that explain features and guide users.
**Typical stakes:** Medium.

Judge these systems over the whole **conversation**. Many failures only show up on turn 3 or later: forgetting a constraint, contradicting an earlier answer, never escalating.

## Failure modes
`misread-intent` · `should-have-asked` · `missed-escalation` · `over-refusal` · `wrong-tone` · `too-long` · `lost-context` · `early-wrong-guess` · `multi-turn-erosion` · `goal-not-reached` · contradicting an earlier turn · `unsupported-claim` · deflection that frustrates (sends the user back to the same article)

## Metrics

| Question | Metric | Grader | How |
|---|---|---|---|
| Right | Resolution correctness | Judge (per conversation) | Was the user's actual issue resolved correctly by the end? |
| Right | Constraint retention | Judge | Constraints stated earlier are honored later |
| Right | Cross-turn consistency | Judge | No contradictions between turns |
| Safe | Escalation correctness | Code + judge | Escalates when policy says to (billing disputes, legal, distress, repeated failure); does not escalate trivial cases |
| Right | Handoff quality | Judge | Summary passed to a human agent is complete and accurate |
| Safe | Policy and tone compliance | Judge | Brand voice, no promises outside policy (refunds, SLAs) |
| Worth it | Containment rate | Analytics | Resolved without human; pair with CSAT so containment is not bought by stonewalling |
| Worth it | Re-contact within 7 days | Analytics | Strong signal of false resolution |
| Worth it | CSAT / thumbs | Analytics | Segment by intent |

## Dataset design
- **Replay real conversations** (anonymized) and also **simulate** them: a user-simulator LLM with a goal, persona and hidden facts revealed only when asked.
- Slices by intent (top 20 intents cover most volume), by persona (frustrated, vague, expert, non-native), and by length (1 turn, 3 to 5 turns, 8+ turns).
- Include "should escalate" scenarios: angry customer, legal threat, safety issue, account security, repeated failure.

## Pass bars (Medium stakes default)
- Resolution correctness >= 85% overall and >= 75% on every top-10 intent (no intent left behind)
- Escalation recall >= 95% on must-escalate slice
- 0 out-of-policy commitments
- Online: containment up without CSAT or re-contact getting worse

## Tip
Read the conversations where containment succeeded but the user re-contacted later. Those are the cases where your offline evals are most likely to be misleading you.
