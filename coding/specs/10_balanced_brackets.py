from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 10
TITLE = "Balanced Brackets"
LEVEL = "easy"
TOPIC = "stack"
FUNC = "is_balanced"
SIGNATURE = "def is_balanced(s: str) -> bool:"
STATEMENT = """
`s` contains only the characters `()[]{}`. Return `True` if every opening
bracket is closed by the same type of bracket in the correct order, otherwise
`False`. The empty string is balanced.
"""
CONSTRAINTS = """
- `0 <= len(s) <= 2 * 10**5`
"""
EXAMPLES = [dict(s="{[]}()"), dict(s="([)]")]

PAIRS = {"(": ")", "[": "]", "{": "}"}


def edge_cases():
    return [dict(s=""), dict(s="("), dict(s=")"), dict(s=")("), dict(s="()[]{}"), dict(s="(((("),
            dict(s="{[()()]}"), dict(s="(]"), dict(s="(()")]


def _balanced(rng, pairs):
    out, stack = [], []
    while pairs or stack:
        if pairs and (not stack or rng.random() < 0.5):
            o = rng.choice("([{")
            out.append(o)
            stack.append(PAIRS[o])
            pairs -= 1
        else:
            out.append(stack.pop())
    return out


def random_case(rng):
    s = _balanced(rng, rng.randint(0, 6))
    if s and rng.random() < 0.5:
        i = rng.randrange(len(s))
        r = rng.random()
        if r < 0.4:
            s[i] = rng.choice("()[]{}")
        elif r < 0.7:
            del s[i]
        else:
            s[i], s[-1] = s[-1], s[i]
    return dict(s="".join(s))


def perf_case(rng):
    opens = [rng.choice("([{") for _ in range(100000)]
    return dict(s="".join(opens) + "".join(PAIRS[o] for o in reversed(opens)))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['s'], 0, 2 * 10**5) and set(c['s']) <= set('()[]{}')
