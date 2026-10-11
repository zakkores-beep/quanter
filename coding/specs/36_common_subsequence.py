from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 36
TITLE = "Longest Common Subsequence"
LEVEL = "medium"
TOPIC = "2-D dynamic programming"
FUNC = "common_subsequence"
SIGNATURE = "def common_subsequence(a: str, b: str) -> int:"
STATEMENT = """
Return the length of the longest string that is a subsequence of both `a`
and `b` (characters keep their order but need not be adjacent).
"""
CONSTRAINTS = """
- `0 <= len(a), len(b) <= 500`
- lowercase letters only
"""
EXAMPLES = [dict(a="market", b="marker"), dict(a="abc", b="def")]


def edge_cases():
    return [dict(a="", b="abc"), dict(a="abc", b="abc"), dict(a="abc", b="cba"), dict(a="aaaa", b="aa"),
            dict(a="abcde", b="ace"), dict(a="z", b="")]


def random_case(rng):
    return dict(a="".join(rng.choice("abc") for _ in range(rng.randint(0, 8))),
                b="".join(rng.choice("abc") for _ in range(rng.randint(0, 8))))


def perf_case(rng):
    return dict(a="".join(rng.choice("abcd") for _ in range(500)), b="".join(rng.choice("abcd") for _ in range(500)))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return all(size(c[k], 0, 500) and set(c[k]) <= set('abcdefghijklmnopqrstuvwxyz') for k in ('a', 'b'))
