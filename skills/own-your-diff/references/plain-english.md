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

## Simple first, technical only when needed

Say what happens in everyday words first. Add the technical term or detail only when the reader needs it.

- Start with what the change does for a person: "Before, you could push code nobody had read. Now the push stops until you pass a short quiz."
- Then give the technical version, if the reader needs it: "The pre-push hook runs `quizgate check`, which looks up each commit in the ledger."
- A technical detail earns its place only if the reader needs it to follow the next step, to change the code, or to answer the quiz. If not, cut it.
- Give a number, a file, or a line of code instead of an adjective. "Pushes now take 40 ms longer", not "a small cost".
- Never explain a simple thing with a hard word. If a 12-year-old could follow the plain version, use the plain version.

## No AI fluff

AI fluff is text that sounds smart but tells the reader nothing. Every sentence must say a fact about this change: what it does, why, what it costs, or what can go wrong. A sentence you could paste into a walkthrough of a different change is fluff. Delete it.

Do not write:

- **Throat-clearing.** "Let's dive in", "In this section we will explore", "It's worth noting that", "It is important to understand". Say the thing.
- **Summaries of what you just said.** "In summary", "In short", "Overall", "To recap". The page is short. The reader remembers.
- **Praise and hype.** "elegant", "powerful", "clean", "crucial", "game-changer", "best practice". Say what it does and let the reader judge.
- **Empty contrast.** "This isn't just X, it's Y." "Not only X, but also Y." Say Y.
- **Lists of three for rhythm.** "fast, safe, and simple". Keep only the items that are true and matter, with evidence.
- **Hedges.** "may help", "can potentially", "aims to", "is designed to". Say what the code does. If you do not know, say so once and plainly.
- **Vague nouns.** "landscape", "ecosystem", "journey", "realm", "tapestry", "space" (for "area"). Name the real thing.
- **Grand verbs.** "delve", "unlock", "empower", "elevate", "streamline", "harness", "foster", "underscore", "navigate". Use the plain verb.
- **Dashes for drama.** An em dash (—) to set up a reveal. Use a period.

`plainlint` notes the words and phrases it can find from these lists. It cannot find all fluff. Reread each sentence and ask: "What fact does this tell the reader?" No fact, no sentence.

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
- Does every sentence tell a fact about this change? Is any of it AI fluff?
- Did it go technical only where the reader needs it?
- Can I cut a word, a sentence, or the whole lesson and lose nothing?
