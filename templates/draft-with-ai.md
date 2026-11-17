# Draft your Eval PRD with AI

Paste the prompt below into Claude, ChatGPT, Gemini, Cursor or any AI assistant you use at work. Then paste the [Eval PRD template](eval-prd.md) under it, or attach the file. The assistant interviews you and drafts the document. If you answer each question, plan on 30 to 45 minutes. If you only have five minutes, give short answers or say "just write it", and it drafts from what it has, marks its guesses and tells you what to fill in first.

The draft is a starting point. The example cases are only as good as the real tickets and logs you give it, and the stakes and pass bars are decisions you own. Check every line marked **[check]** with your team before engineers build from it.

If your company doesn't allow customer data in an AI assistant, remove names and account details from the examples before you paste them.

---

```text
You are helping a product manager write an Eval PRD for an AI feature. An Eval
PRD tells engineers what the feature should do, what to test, what "done" means
and what to watch once it's live. The template is below this prompt. Follow its
nine sections and its hints.

How to work:

1. Start with one message of five quick questions: what the feature does
   and for whom; new launch or improvement; whether it only answers or also
   takes actions; whether a person checks its output before it takes
   effect; and the worst thing it could do. Then go through the template's
   sections in order, with no more than three questions per message.

   If I answer in a few words, or ask you to just write it, stop asking and
   draft the whole document right away. Fill gaps with your best guess
   marked [check], and end with a short list of what I should fill in
   first. Never ask the same question twice. If I skip one, guess and
   mark it [check].

2. Push for real examples. When we reach example cases (section 5), ask me to
   paste real support tickets, search logs, chat transcripts or notes from the
   manual workflow. Build cases from those. If I have none, propose cases and
   mark each one [check].

3. Cover conversations. Most AI features fail across several turns more than
   in one reply. Propose at least three short conversations of two to four
   turns: one where the user adds or changes a detail partway through, one where
   the user pushes on a rule from section 3 over several turns, and one that
   ends in a handoff to a person. Give the expected behavior at each turn.

4. Make every rule testable. For sections 2 and 3, rewrite anything vague until
   a person could hold one reply, or one whole conversation, up against it and
   say yes or no.

5. Keep section 3 short. Aim for three to eight rules, each one you could
   see broken in a single reply or action. Requirements on the system, such
   as logging or audit records, go to section 9 or the open questions.

6. Set the stakes from what the feature does. Match it to a row of the
   template's stakes table, using what I've told you and what plainly
   follows from it. For example, an agent that changes records with no one
   checking can do costly harm, and a feature that reads customer messages
   handles personal data, even if I don't say so. If it fits two rows, pick the higher one. Don't raise the level
   for something that only might be true. List it as an open question and
   say which level it would move the feature to. A person who reviews every
   output counts as a review, even if some people may skim. If the feature
   takes actions and I haven't said whether a person checks them first,
   assume nobody does. Explain the level in one sentence.

7. Fill section 7 from the default bars for that level, and say which
   numbers I should question. Any conversation that pushes on a section 3
   rule is a safety case: its bar is zero failures across every run, the
   same as the rule itself.

8. Don't invent facts about my product, metrics or users. When you have to
   guess, write the guess and mark it [check].

9. Keep the interview moving. Don't reprint drafted sections while we talk.
   Confirm what you captured in a line or two and move on. Ask about
   sections 8 and 9 together.

10. When the interview is done, write the whole Eval PRD in Markdown, in
    plain language a PM could read on a phone. Keep the "For engineers"
    section at the end. After the document, list the open questions I should
    take to my engineering lead. Then offer to turn sections 3, 5 and 7 into
    eval-prd.yaml and test cases, if I paste eval-prd.yaml and
    golden-case.schema.json from the repo.

Start by asking your first questions.
```
