# 31. Non-Adjacent Trading Days

**Difficulty:** medium · **Topic:** 1-D dynamic programming

`gains[i] >= 0` is what you earn by trading on day `i`, but you may never
trade on two consecutive days. Return the largest total you can earn.

## Function

```python
def max_non_adjacent(gains: list[int]) -> int:
```

## Constraints

- `0 <= len(gains) <= 2 * 10**5`
- `0 <= gains[i] <= 10**4`

## Examples

**Example 1**

```
Input:  gains = [4, 1, 1, 4]
Output: 8
```

**Example 2**

```
Input:  gains = [2, 7, 9, 3, 1]
Output: 12
```

## Run

```
python judge.py 31
```
