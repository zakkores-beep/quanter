# 3. P&L Windows Hitting Target

**Difficulty:** medium · **Topic:** arrays & hashing

`pnl[i]` is the profit (possibly negative) on day `i`. Count the contiguous,
non-empty ranges of days whose total profit is exactly `k`.

## Function

```python
def count_subarrays(pnl: list[int], k: int) -> int:
```

## Constraints

- `1 <= len(pnl) <= 2 * 10**5`
- `-1000 <= pnl[i] <= 1000`
- `-10**9 <= k <= 10**9`

## Examples

**Example 1**

```
Input:  pnl = [3, 4, 7, -7, 2], k = 7
Output: 3
```

**Example 2**

```
Input:  pnl = [1, -1, 1, -1], k = 0
Output: 4
```

## Run

```
python judge.py 3
```
