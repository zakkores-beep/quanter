# 25. Merge Trading Sessions

**Difficulty:** medium · **Topic:** intervals

Each interval `[start, end]` (with `start <= end`) is a closed time range.
Merge all intervals that overlap **or touch** (`[1, 3]` and `[3, 5]` become
`[1, 5]`). Return the merged intervals sorted by start.

## Function

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
```

## Constraints

- `0 <= len(intervals) <= 10**5`
- `0 <= start <= end <= 10**9`

## Examples

**Example 1**

```
Input:  intervals = [[8, 10], [1, 3], [2, 6], [15, 18]]
Output: [[1, 6], [8, 10], [15, 18]]
```

**Example 2**

```
Input:  intervals = [[1, 3], [3, 5]]
Output: [[1, 5]]
```

## Run

```
python judge.py 25
```
