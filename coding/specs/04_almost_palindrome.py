from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 4
TITLE = "Almost a Palindrome"
LEVEL = "easy"
TOPIC = "two pointers"
FUNC = "almost_palindrome"
SIGNATURE = "def almost_palindrome(s: str) -> bool:"
STATEMENT = """
Return `True` if `s` reads the same forwards and backwards after deleting
**at most one** character, otherwise `False`.
"""
CONSTRAINTS = """
- `1 <= len(s) <= 2 * 10**5`
- `s` contains only lowercase English letters
"""
EXAMPLES = [dict(s="abca"), dict(s="abc"), dict(s="racecar")]


def edge_cases():
    return [dict(s="a"), dict(s="ab"), dict(s="aab"), dict(s="baa"), dict(s="abcdba"), dict(s="abcdcbxa"),
            dict(s="xabcdcbax"), dict(s="abxcba"), dict(s="abxycba")]


def _palindrome(rng, n, letters):
    half = [rng.choice(letters) for _ in range(n // 2)]
    mid = [rng.choice(letters)] if n % 2 else []
    return half + mid + half[::-1]


def random_case(rng):
    r = rng.random()
    if r < 0.6:
        s = _palindrome(rng, rng.randint(1, 9), "abc")
        for _ in range(1 if r < 0.4 else 2):
            s.insert(rng.randint(0, len(s)), rng.choice("abc"))
        return dict(s="".join(s))
    return dict(s="".join(rng.choice("ab") for _ in range(rng.randint(1, 10))))


def perf_case(rng):
    s = _palindrome(rng, 199999, "ab")
    s.insert(100003, "c")
    return dict(s="".join(s))


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['s'], 1, 2 * 10**5) and set(c['s']) <= set('abcdefghijklmnopqrstuvwxyz')
