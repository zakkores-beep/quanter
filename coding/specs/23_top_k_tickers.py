from gentools import grid, ints, nondecreasing, size, tree  # noqa: F401
ID = 23
TITLE = "Most Traded Tickers"
LEVEL = "medium"
TOPIC = "heaps"
FUNC = "top_k_tickers"
SIGNATURE = "def top_k_tickers(trades: list[str], k: int) -> list[str]:"
STATEMENT = """
`trades` lists the ticker of every trade. Return the `k` most frequently
traded tickers, ordered by count (highest first); break ties alphabetically
(`"ABC"` before `"ABD"`).
"""
CONSTRAINTS = """
- `1 <= len(trades) <= 2 * 10**5`
- tickers are 1-5 uppercase letters
- `1 <= k <=` number of distinct tickers
"""
EXAMPLES = [dict(trades=["GS", "MS", "GS", "JPM", "MS", "C"], k=2), dict(trades=["B", "A", "C"], k=3)]

POOL = ["AAPL", "MSFT", "GS", "JPM", "TSLA", "NVDA"]


def edge_cases():
    return [dict(trades=["AAPL"], k=1), dict(trades=["B", "A", "B", "C", "A"], k=2),
            dict(trades=["Z", "Y", "X", "Z"], k=3), dict(trades=["AB", "A", "ABC", "A", "AB", "ABC"], k=2)]


def random_case(rng):
    trades = [rng.choice(POOL) for _ in range(rng.randint(1, 12))]
    return dict(trades=trades, k=rng.randint(1, len(set(trades))))


def perf_case(rng):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pool = sorted({"".join(rng.choice(letters) for _ in range(4)) for _ in range(5000)})
    return dict(trades=[rng.choice(pool) for _ in range(200000)], k=100)


def valid(c):
    """Does this input satisfy the stated constraints?"""
    return size(c['trades'], 1, 2 * 10**5) and all(1 <= len(t) <= 5 and t.isalpha() and t.isupper() for t in c['trades']) and 1 <= c['k'] <= len(set(c['trades']))
