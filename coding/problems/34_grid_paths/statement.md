# 34. Paths Through a Blocked Grid

**Difficulty:** medium · **Topic:** 2-D dynamic programming

`grid` is a list of equal-length strings; `'.'` is open and `'#'` is blocked.
Starting at the top-left cell, you may only move **right** or **down**, and
only through open cells. Return the number of different paths to the
bottom-right cell, modulo `10**9 + 7`. If the start or end cell is blocked,
the answer is 0.

## Function

```python
def count_paths(grid: list[str]) -> int:
```

## Constraints

- `1 <= rows, cols <= 300`

## Examples

**Example 1**

```
Input:  grid = ['...', '.#.', '...']
Output: 2
```

**Example 2**

```
Input:  grid = ['.#', '#.']
Output: 0
```

## Run

```
python judge.py 34
```
