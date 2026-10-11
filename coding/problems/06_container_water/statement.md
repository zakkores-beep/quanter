# 6. Widest Price Channel

**Difficulty:** medium · **Topic:** two pointers

Pick two indices `i < j`. The channel between them has area
`min(heights[i], heights[j]) * (j - i)`. Return the largest possible area.

## Function

```python
def max_area(heights: list[int]) -> int:
```

## Constraints

- `2 <= len(heights) <= 2 * 10**5`
- `0 <= heights[i] <= 10**4`

## Examples

**Example 1**

```
Input:  heights = [3, 1, 2, 4, 5]
Output: 12
```

**Example 2**

```
Input:  heights = [1, 1]
Output: 1
```

## Run

```
python judge.py 6
```
