# 15. Integer Square Roots

**Difficulty:** easy · **Topic:** binary search

For each `x` in `nums`, return the largest integer `r` with `r * r <= x`.

Do **not** use `math.sqrt`, `math.isqrt` or `** 0.5`: use binary search on
integers. (Floating point gives wrong answers near `10**18` - try it.)

## Function

```python
def isqrt_all(nums: list[int]) -> list[int]:
```

## Constraints

- `1 <= len(nums) <= 10**4`
- `0 <= nums[i] <= 10**18`

## Examples

**Example 1**

```
Input:  nums = [0, 1, 8, 9, 10, 99]
Output: [0, 1, 2, 3, 3, 9]
```

## Run

```
python judge.py 15
```
