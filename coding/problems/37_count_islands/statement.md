# 37. Count the Islands

**Difficulty:** medium · **Topic:** graphs

`grid` is a list of equal-length strings of `'1'` (land) and `'0'` (water).
An island is a group of land cells connected up, down, left or right (not
diagonally). Return the number of islands.

## Function

```python
def count_islands(grid: list[str]) -> int:
```

## Constraints

- `1 <= rows, cols <= 400`
- Python's default recursion limit is 1000: a recursive DFS can crash on big islands.

## Examples

**Example 1**

```
Input:  grid = ['11000', '11000', '00100', '00011']
Output: 3
```

**Example 2**

```
Input:  grid = ['101', '010', '101']
Output: 5
```

## Run

```
python judge.py 37
```
