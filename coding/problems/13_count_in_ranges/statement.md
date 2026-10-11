# 13. Price Range Queries

**Difficulty:** easy · **Topic:** binary search

`prices` is sorted in non-decreasing order. Each query is `[lo, hi]` with
`lo <= hi`. For each query, return how many prices `p` satisfy
`lo <= p <= hi`.

You may use the `bisect` module, but practise writing the binary search
yourself too.

## Function

```python
def count_in_ranges(prices: list[int], queries: list[list[int]]) -> list[int]:
```

## Constraints

- `0 <= len(prices) <= 10**5`, sorted non-decreasing
- `1 <= len(queries) <= 10**5`
- `-10**9 <= prices[i], lo, hi <= 10**9`

## Examples

**Example 1**

```
Input:  prices = [1, 2, 2, 2, 3, 7], queries = [[2, 2], [1, 3], [4, 6], [0, 100]]
Output: [3, 5, 0, 6]
```

## Run

```
python judge.py 13
```
