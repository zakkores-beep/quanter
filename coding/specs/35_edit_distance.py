from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 35
TITLE = "Ticker Edit Distance"
LEVEL = "medium"
TOPIC = "2-D dynamic programming"
FUNC = "edit_distance"
SIGNATURE = "def edit_distance(a: str, b: str) -> int:"
STATEMENT = """
Return the minimum number of single-character edits (insert a character,
delete a character, or replace a character) that turn `a` into `b`.
"""
CONSTRAINTS = """
- `0 <= len(a), len(b) <= 500`
- lowercase letters only
"""
EXAMPLES = [dict(a="spread", b="bread"), dict(a="trade", b="trader")]


def edge_cases():
    return [dict(a="", b=""), dict(a="", b="abc"), dict(a="abc", b=""), dict(a="same", b="same"),
            dict(a="ab", b="ba"), dict(a="abc", b="xyz"), dict(a="aaaa", b="aa")]


def random_case(rng):
    return dict(a="".join(rng.choice("abc") for _ in range(rng.randint(0, 5))),
                b="".join(rng.choice("abc") for _ in range(rng.randint(0, 5))))


def perf_case(rng):
    return dict(a="".join(rng.choice("abcd") for _ in range(500)), b="".join(rng.choice("abcd") for _ in range(500)))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return all(size(c[k], 0, 500) and set(c[k]) <= set('abcdefghijklmnopqrstuvwxyz') for k in ('a', 'b'))
