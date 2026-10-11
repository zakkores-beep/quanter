# 23. Most Traded Tickers

**Difficulty:** medium · **Topic:** heaps

`trades` lists the ticker of every trade. Return the `k` most frequently
traded tickers, ordered by count (highest first); break ties alphabetically
(`"ABC"` before `"ABD"`).

## Function

```python
def top_k_tickers(trades: list[str], k: int) -> list[str]:
```

## Constraints

- `1 <= len(trades) <= 2 * 10**5`
- tickers are 1-5 uppercase letters
- `1 <= k <=` number of distinct tickers

## Examples

**Example 1**

```
Input:  trades = ['GS', 'MS', 'GS', 'JPM', 'MS', 'C'], k = 2
Output: ['GS', 'MS']
```

**Example 2**

```
Input:  trades = ['B', 'A', 'C'], k = 3
Output: ['A', 'B', 'C']
```

## Run

```
python judge.py 23
```
