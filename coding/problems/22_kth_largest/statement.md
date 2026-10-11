# 22. k-th Largest Fill

**Difficulty:** easy · **Topic:** heaps

Return the `k`-th largest value in `fills` (counting duplicates, so for
`[7, 7, 1]` the 2nd largest is 7).

Try a min-heap of size `k` (`heapq`) instead of sorting everything.

## Function

```python
def kth_largest(fills: list[int], k: int) -> int:
```

## Constraints

- `1 <= k <= len(fills) <= 2 * 10**5`
- `-10**9 <= fills[i] <= 10**9`

## Examples

**Example 1**

```
Input:  fills = [7, 7, 7, 1], k = 2
Output: 7
```

**Example 2**

```
Input:  fills = [3, 1, 4, 1, 5, 9, 2, 6], k = 3
Output: 5
```

## Run

```
python judge.py 22
```
