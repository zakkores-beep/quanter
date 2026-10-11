from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 8
TITLE = "Longest Run Without Repeats"
LEVEL = "medium"
TOPIC = "sliding window"
FUNC = "longest_unique"
SIGNATURE = "def longest_unique(s: str) -> int:"
STATEMENT = """
Return the length of the longest substring (contiguous) of `s` in which no
character appears twice.
"""
CONSTRAINTS = """
- `0 <= len(s) <= 2 * 10**5`
- `s` contains lowercase letters and digits
"""
EXAMPLES = [dict(s="xyzxyzz"), dict(s="abba")]


def edge_cases():
    return [dict(s=""), dict(s="a"), dict(s="aaaa"), dict(s="abcdef"), dict(s="abcbade"), dict(s="a1b2a1c"),
            dict(s="dvdf")]


def random_case(rng):
    return dict(s="".join(rng.choice("abcd") for _ in range(rng.randint(0, 12))))


def perf_case(rng):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return dict(s="".join(rng.choice(chars) for _ in range(200000)))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['s'], 0, 2 * 10**5) and set(c['s']) <= set('abcdefghijklmnopqrstuvwxyz0123456789')
