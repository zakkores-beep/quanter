# 39. Shortest Route Across the Floor

**Difficulty:** medium · **Topic:** graphs

`grid` is a list of equal-length strings; `'.'` is open, `'#'` is a wall.
Moving one cell up, down, left or right costs one step. Return the fewest
steps from the top-left cell to the bottom-right cell, or -1 if it cannot be
reached (including when either cell is a wall).

## Function

```python
def shortest_path(grid: list[str]) -> int:
```

## Constraints

- `1 <= rows, cols <= 400`

## Examples

**Example 1**

```
Input:  grid = ['..#', '#..', '#..']
Output: 4
```

**Example 2**

```
Input:  grid = ['.#', '#.']
Output: -1
```

## Run

```
python judge.py 39
```
