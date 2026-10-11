# 9. Shortest Window to Fill an Order

**Difficulty:** medium · **Topic:** sliding window

`volumes[i]` is the (positive) volume traded in minute `i`. Return the length
of the shortest run of consecutive minutes whose total volume is **at least**
`target`. Return 0 if no such run exists.

## Function

```python
def shortest_window(volumes: list[int], target: int) -> int:
```

## Constraints

- `1 <= len(volumes) <= 2 * 10**5`
- `1 <= volumes[i] <= 10**4`
- `1 <= target <= 10**9`

## Examples

**Example 1**

```
Input:  volumes = [2, 3, 1, 2, 4, 3], target = 7
Output: 2
```

**Example 2**

```
Input:  volumes = [1, 1, 1], target = 5
Output: 0
```

## Run

```
python judge.py 9
```
