# 14. Minimum Settlement Capacity

**Difficulty:** medium · **Topic:** binary search

Trades with sizes `weights` must be settled **in the given order** over at
most `days` days. Each day you settle a contiguous block of the remaining
trades whose total size is at most the daily capacity `C`. A trade cannot
be split.

Return the smallest capacity `C` that settles everything within `days` days.

## Function

```python
def min_capacity(weights: list[int], days: int) -> int:
```

## Constraints

- `1 <= days <= len(weights) <= 5 * 10**4`
- `1 <= weights[i] <= 500`

## Examples

**Example 1**

```
Input:  weights = [3, 2, 2, 4, 1, 4], days = 3
Output: 6
```

**Example 2**

```
Input:  weights = [1, 2, 3, 4, 5], days = 1
Output: 15
```

## Run

```
python judge.py 14
```
