# 5. Zero-Sum Hedge Triplets

**Difficulty:** medium · **Topic:** two pointers

Count the **distinct value triplets** `(a, b, c)` with `a <= b <= c` and
`a + b + c == 0`, where `a`, `b`, `c` come from three different positions
of `nums`. Triplets with the same values are counted once, no matter how
many index combinations produce them.

## Function

```python
def count_zero_triplets(nums: list[int]) -> int:
```

## Constraints

- `0 <= len(nums) <= 1500`
- `-10**5 <= nums[i] <= 10**5`

## Examples

**Example 1**

```
Input:  nums = [-1, 0, 1, 2, -1, -4]
Output: 2
```

**Example 2**

```
Input:  nums = [0, 0, 0, 0]
Output: 1
```

## Run

```
python judge.py 5
```
