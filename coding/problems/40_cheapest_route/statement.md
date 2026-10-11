# 40. Cheapest Currency Route

**Difficulty:** medium · **Topic:** graphs

There are `n` currencies labelled `0 .. n-1`. Each `[u, v, f]` in `fees` is
a one-way conversion from `u` to `v` costing fee `f >= 0`. Return the lowest
total fee to get from `src` to `dst`, or -1 if `dst` is unreachable.
Converting `src` to itself costs 0.

## Function

```python
def cheapest_route(n: int, fees: list[list[int]], src: int, dst: int) -> int:
```

## Constraints

- `1 <= n <= 10**5`
- `0 <= len(fees) <= 2 * 10**5`
- `0 <= f <= 1000`; parallel conversions may exist

## Examples

**Example 1**

```
Input:  n = 3, fees = [[0, 1, 5], [1, 2, 5], [0, 2, 20]], src = 0, dst = 2
Output: 10
```

**Example 2**

```
Input:  n = 2, fees = [[1, 0, 3]], src = 0, dst = 1
Output: -1
```

## Run

```
python judge.py 40
```
