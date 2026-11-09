"""Word lists and text helpers that plainlint and quizlint share.

usage: import plain
  plain.HARD, plain.FLUFF, plain.HARD_RE   the do-not-write and AI-fluff lists of references/plain-english.md
  plain.sentences(text), plain.words(text)
  plain.code_names(text)                   the code names in a text, in order, once each
  plain.giveaway(options)                  the correct option of a single question is much the longest
"""
import re

# The do-not-write list of references/plain-english.md, with the plain word to use.
HARD = {
    "utilize": "write use", "utilise": "write use", "leverage": "write use",
    "facilitate": "write let or help", "orchestrate": "write run",
    "robust": "say what it handles", "seamless": "say what it handles", "seamlessly": "say what it handles",
    "ensure": "write make sure", "in order to": "write to", "prior to": "write before",
    "subsequent to": "write after", "a number of": "write some, or give the number",
    "paradigm": "name the real thing", "synergy": "name the real thing", "holistic": "name the real thing",
    "essentially": "delete it", "basically": "delete it", "simply": "delete it",
}
# The AI-fluff list of references/plain-english.md: text that sounds smart and says nothing.
FLUFF = [
    "let's dive", "dive in", "dive into", "delve", "it's worth noting", "it is worth noting",
    "it's important to", "it is important to", "in this section", "in summary", "to recap",
    "in short", "overall,", "not just", "not only", "game-changer", "game changer", "best practice",
    "elegant", "powerful", "crucial", "unlock", "empower", "elevate", "streamline", "harness",
    "foster", "underscore", "landscape", "ecosystem", "journey", "realm", "tapestry",
    "can potentially", "aims to", "is designed to", "—",
]
for phrase in FLUFF:
    HARD.setdefault(phrase, "AI fluff: say the fact, or cut it")
HARD_RE = re.compile(
    "|".join(r"(?<!\w)" + re.escape(w) + (r"(?!\w)" if w[-1].isalnum() else "") for w in sorted(HARD, key=len, reverse=True)),
    re.IGNORECASE,
)


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9`\"(])", text) if s.strip()]


def words(sentence):
    return re.findall(r"[\w'’/.:@`-]+", sentence)


EXTENSIONS = "json|md|py|ts|js|sh|html|yml|yaml|toml|txt|lock"
# Each rule matches one whole word, after the punctuation around it is cut off.
CODE_RULES = [re.compile(rule) for rule in (
    r"[a-z]+[A-Z]\w*",                                # camelCase: runScenario, writeRun
    r"[A-Z][a-z0-9]+[A-Z]\w*",                        # PascalCase with a capital inside: RunResult
    r"(?=.*[A-Za-z])_*[A-Za-z0-9]+(?:_+[A-Za-z0-9]+)+_*",  # snake_case, SCREAMING_SNAKE: core__call_tool
    r"[A-Za-z_][\w.]*\((?!s\))[^()]*\)",              # a call: check(), check(run), but not option(s)
    r"--[A-Za-z][\w-]*|-[A-Za-z]",                    # a flag: --no-verify, -q
    rf"[\w.-]*\w\.(?:{EXTENSIONS})",                  # a file name: run.json, SKILL.md
    r"(?:~|\.\.?)?/[\w.-][\w./-]*",                   # a path from the root, home, or here: ~/.local/bin
    r"(?=.*\.)[\w.-]+(?:/[\w.-]+)+/?",                # a path with a dot in it: .git/hooks/pre-push
    r"[\w.-]+(?:/[\w.-]+){2,}/?|[\w.-]+(?:/[\w.-]+)*/",  # a path of three parts, or ending in /
    r"\.[A-Za-z][\w.-]*",                             # a dot file: .own-your-diff
    r"[A-Za-z_]\w+(?:\.[A-Za-z_]\w+)+",               # a dotted key: core.hooksPath, but not e.g. or 0.2.0
)]
# Brand names that look like camelCase or a file name but are plain words to a reader.
BRANDS = {"GitHub", "GitLab", "JavaScript", "TypeScript", "OpenAI", "PyPI", "macOS", "iOS", "Node.js"}


def code_names(text):
    """The code names in a text, in order, once each."""
    found = re.findall(r"`[^`]+`", text)
    for token in re.sub(r"`[^`]+`", " ", text).split():
        token = token.lstrip("(\"'“‘[").rstrip(",;:!?\"'”’]")
        token = re.sub(r"['’]s$", "", token.rstrip("."))
        while token.endswith(")") and token.count(")") > token.count("("):
            token = token[:-1].rstrip(".,;:")
        if token not in BRANDS and any(rule.fullmatch(token) for rule in CODE_RULES):
            found.append(token)
    return list(dict.fromkeys(found))


def giveaway(options):
    """True when the one correct label is much longer than every wrong one."""
    right = [len(words(o["label"])) for o in options if o.get("correct") is True]
    wrong = [len(words(o["label"])) for o in options if o.get("correct") is not True]
    if len(right) != 1 or not wrong:
        return False
    return right[0] > 1.5 * max(wrong) and right[0] - max(wrong) >= 4
