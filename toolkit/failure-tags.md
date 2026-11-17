# Failure Tags

*Used in the **Discover** stage of [the Loop](../framework/the-loop.md).*

When you review traces, start by writing a short note in your own words about what went wrong. Once you have a few dozen notes, group them and give each group a tag. Shared tags matter because they let you count: "wrong-source showed up in 9% of traces this week" is something a team can act on.

The tags below are a starting set for enterprise SaaS. Use the ones that fit, rename them in your team's language, and add your own. Each tag maps to one of the [three questions](../framework/the-three-questions.md) (is the AI right, safe, worth it), which tells you where its check belongs.

## Grounding · Right
| Tag | What it looks like |
|---|---|
| `unsupported-claim` | States a policy limit that isn't in any retrieved document |
| `wrong-source` | Answers from the 2025 handbook when the 2026 one exists |
| `citation-mismatch` | Cites a document that doesn't contain the claim |

## Retrieval · Right
| Tag | What it looks like |
|---|---|
| `missed-document` | The right document exists but isn't in the top results |
| `noisy-context` | The right passage was retrieved but buried among irrelevant ones and ignored |
| `stale-index` | The document changed at the source and the index wasn't refreshed |

## Understanding · Right
| Tag | What it looks like |
|---|---|
| `misread-intent` | Explains how to upgrade when the user asked whether they're already on that plan |
| `missed-constraint` | Ignores "on the Pro plan" or "for guest users" |
| `should-have-asked` | Guesses on an ambiguous request instead of asking a clarifying question |

## Across a conversation · Right
These only show up when you read the whole conversation, so tag them when you review full sessions as well as single replies.
| Tag | What it looks like |
|---|---|
| `lost-context` | Forgets something the user said three messages ago, such as the board being shared with guests |
| `early-wrong-guess` | Commits to a guess in the first reply and never recovers once the user clarifies |
| `multi-turn-erosion` | Holds a rule on the first ask, then gives in when the user rephrases or pushes over several turns. When the rule is one of your safety rules, count it under safe |
| `goal-not-reached` | Every reply looks fine, yet the user ends the conversation without what they came for |

## Tools and actions · Right
| Tag | What it looks like |
|---|---|
| `wrong-tool` | Searches help articles when it should look up the customer's account |
| `bad-arguments` | Passes the wrong customer ID or date format |
| `stuck-or-gave-up` | Repeats the same call, or abandons a task it could have finished |
| `false-success` | Tells the user the task is done when it isn't |

## Data and SQL · Right
| Tag | What it looks like |
|---|---|
| `wrong-metric-definition` | Counts contractors in "headcount" when the business definition excludes them |
| `wrong-join-or-filter` | Double-counts after joining to a table with several rows per record |
| `silent-empty-result` | Reports "0" without noticing the filter matched nothing |

## Communication · Right
| Tag | What it looks like |
|---|---|
| `wrong-tone` | Casual tone in a draft of a formal warning letter |
| `too-long` | The correct answer is buried in five paragraphs |
| `broken-format` | Invalid JSON, or a required section is missing |
| `over-refusal` | Refuses a reasonable request it could have answered |

## Access and privacy · Safe
| Tag | What it looks like |
|---|---|
| `cross-role-leak` | An employee sees content meant only for managers |
| `cross-tenant-leak` | Customer A's data appears in Customer B's answer |
| `leak-by-paraphrase` | Refuses to show a restricted document but repeats what it says |
| `personal-data-exposed` | Echoes sensitive personal details that the answer didn't need |

## Policy and safety · Safe
| Tag | What it looks like |
|---|---|
| `policy-violation` | Gives medical, legal or tax advice the product must not give |
| `missed-escalation` | Should have handed off to a person and didn't |
| `unconfirmed-action` | Sends an email or updates a record without asking the user first |

## Security · Safe
| Tag | What it looks like |
|---|---|
| `injection-followed` | Obeys instructions hidden in a retrieved document, email or tool output |
| `hidden-context-exposed` | Reveals its system prompt or internal configuration |

## Memory · Right and Safe
| Tag | What it looks like |
|---|---|
| `stale-memory` | Uses an old preference after the user updated it |
| `memory-bleed` | Applies one user's memory to another user |
| `failed-to-forget` | Recalls something the user asked it to delete |

## Fairness · Safe
| Tag | What it looks like |
|---|---|
| `uneven-quality` | Accuracy drops for non-native English or for certain names |
| `protected-attribute-used` | A recommendation changes with gender or age when it shouldn't |

## Deciding what to fix first

Rank failure modes by how often they show up and how much harm each one does. Some tags get a check no matter how rare they are: anything in **Access and privacy**, **Security** or **Fairness** at Medium or High stakes, because a single occurrence can be an incident.
