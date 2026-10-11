# 1. Matching Trade Pairs

**Difficulty:** easy · **Topic:** arrays & hashing

You are given a list of trade prices and a target value. Count the pairs of
indices `(i, j)` with `i < j` such that `prices[i] + prices[j] == target`.

Different index pairs count separately, even if their values are the same.

## Function

```python
def count_pairs(prices: list[int], target: int) -> int:
```

## Constraints

- `0 <= len(prices) <= 2 * 10**5`
- `-10**9 <= prices[i], target <= 10**9`

## Examples

**Example 1**

```
Input:  prices = [1, 5, 3, 3, 7], target = 6
Output: 2
```

**Example 2**

```
Input:  prices = [2, 2, 2], target = 4
Output: 3
```

## Run

```
python judge.py 1
```
