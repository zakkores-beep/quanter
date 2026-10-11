# 26. Insert a Blackout Window

**Difficulty:** medium · **Topic:** intervals

`intervals` is sorted by start and contains closed intervals that neither
overlap nor touch. Insert the closed interval `new`, merging wherever
intervals overlap **or touch**, and return the sorted result.

Aim for O(n): the input is already sorted.

## Function

```python
def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
```

## Constraints

- `0 <= len(intervals) <= 10**5`
- `0 <= start <= end <= 10**9` for every interval, including `new`

## Examples

**Example 1**

```
Input:  intervals = [[1, 2], [5, 6], [9, 12]], new = [3, 5]
Output: [[1, 2], [3, 6], [9, 12]]
```

**Example 2**

```
Input:  intervals = [], new = [4, 8]
Output: [[4, 8]]
```

## Run

```
python judge.py 26
```
