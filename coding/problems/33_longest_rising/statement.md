# 33. Longest Rising Subsequence

**Difficulty:** medium · **Topic:** 1-D dynamic programming

Return the length of the longest **strictly increasing** subsequence of
`prices` (elements keep their order but need not be adjacent).

The O(n^2) DP is too slow for the largest test; you need O(n log n).

## Function

```python
def longest_rising(prices: list[int]) -> int:
```

## Constraints

- `0 <= len(prices) <= 2 * 10**5`
- `-10**9 <= prices[i] <= 10**9`

## Examples

**Example 1**

```
Input:  prices = [0, 8, 4, 12, 2, 10, 6, 14]
Output: 4
```

**Example 2**

```
Input:  prices = [3, 3, 3]
Output: 1
```

## Run

```
python judge.py 33
```
