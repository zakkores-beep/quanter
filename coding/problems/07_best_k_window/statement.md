# 7. Best k-Day Window

**Difficulty:** easy · **Topic:** sliding window

Return the largest total of `k` consecutive values in `pnl`.

## Function

```python
def best_window(pnl: list[int], k: int) -> int:
```

## Constraints

- `1 <= k <= len(pnl) <= 2 * 10**5`
- `-10**4 <= pnl[i] <= 10**4`

## Examples

**Example 1**

```
Input:  pnl = [4, -1, 4, -10, 8], k = 2
Output: 3
```

**Example 2**

```
Input:  pnl = [-3, -1, -2], k = 2
Output: -3
```

## Run

```
python judge.py 7
```
