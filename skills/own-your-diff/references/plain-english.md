# Plain English for the walkthrough

The reader is new to this part of the code. They are smart but busy. Write so that they understand each sentence the first time they read it. The model is ASD-STE100 (Simplified Technical English) and Orwell's six rules.

## Sentences

- One idea per sentence. Keep a sentence to 20 words or fewer. `plainlint` notes longer ones.
- Use the active voice. Name who does what: "the hook runs `quizgate`", not "`quizgate` is run".
- Use the present tense for what the code does: "the gate blocks the push".
- Put the main point first. The reason or condition comes after it.
- Give steps as a numbered list, one action per step, in the order they happen.
- Keep a paragraph to 5 sentences or fewer.

## Words

- Use the short, common word. Use the words a colleague would say aloud at a whiteboard.
- One word for one thing. If you call it "the ledger" once, call it "the ledger" every time. Never switch to "the record" or "the store".
- One meaning for one word. Do not use "check" for both the hook and the act of reading a file.
- Use a noun for a thing and a verb for an action. Write "the hook checks the file", not "the hook performs a check of the file".
- Name the real thing. Write "the pre-push hook", not "the mechanism" or "the component".
- No metaphor, idiom, or marketing words. A word from the list below is a note in `plainlint`.

| Do not write | Write |
|---|---|
| utilize, leverage | use |
| facilitate, enable | let, help, make possible |
| orchestrate | run, call in order |
| robust, seamless | say what it handles: "works when the network fails" |
| ensure | make sure |
| in order to | to |
| prior to, subsequent to | before, after |
| a number of | some, or the number |
| paradigm, synergy, holistic | say the real thing |
| essentially, basically, simply, just | delete it |

## New terms

- Introduce a new term only when the reader needs it, and only one new term at a time.
- Define it in one plain sentence the first time it appears: "A **patch-id** is a hash of what a commit changes, not of its message or date."
- Show it before you name it. First the concrete case, then the name, then the rule.
- If the page needs more than 5 new terms, list them in the "Words on this page" box at the top.
- Do not use a term from the code (a class, a flag, a file name) as if the reader knows it. Say what it is the first time.

## Order: from the top down

Explain from the outside in, and never skip a level.

1. **The system.** What the whole system does, who uses it, and which part this change touches. No code.
2. **The part.** The parts inside the touched area, and how they talk. Mark what is new or changed.
3. **The code.** The functions, data, and lines that carry the change.

A reader must understand a level before the next one starts. Each lesson stays at one level. A lesson at a lower level starts by saying which box of the level above it opens.

## Diagrams

- Draw one diagram per level, from the top down. The first diagram shows the whole system. Each diagram after it opens one box of the diagram before it, and its caption says which.
- Put 3 to 7 boxes in a diagram. More boxes mean you need another level.
- Label each box with a plain noun ("pre-push hook", "ledger file"). Label each arrow with a plain verb ("reads", "blocks", "writes").
- Mark the new and changed parts with the `new` class. Everything else uses `box`.
- Arrows go left to right or top to bottom, in the order things happen.
- The caption says in one sentence what to notice.

## Check before you hand it over

Read the page as the reader. For each lesson, ask:

- Does it teach one idea, and does its first sentence say which idea?
- Does it use a word that the page has not yet explained?
- Can I cut a word, a sentence, or the whole lesson and lose nothing?
