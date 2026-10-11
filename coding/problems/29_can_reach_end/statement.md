# 29. Reach the Last Checkpoint

**Difficulty:** medium · **Topic:** greedy

You start at index 0. From index `i` you may move forward by any number of
steps from 0 to `jumps[i]`. Return `True` if you can reach the last index.

## Function

```python
def can_reach_end(jumps: list[int]) -> bool:
```

## Constraints

- `1 <= len(jumps) <= 2 * 10**5`
- `0 <= jumps[i] <= 10**5`

## Examples

**Example 1**

```
Input:  jumps = [2, 0, 1, 0]
Output: True
```

**Example 2**

```
Input:  jumps = [2, 1, 0, 3]
Output: False
```

## Run

```
python judge.py 29
```
