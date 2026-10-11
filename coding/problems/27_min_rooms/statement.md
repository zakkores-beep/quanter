# 27. Meeting Rooms Needed

**Difficulty:** medium · **Topic:** intervals

Each meeting `[start, end]` occupies a room for the half-open time range
`start <= t < end` (a meeting ending at 10 frees its room for one starting
at 10). Return the minimum number of rooms needed to hold all meetings.

## Function

```python
def min_rooms(meetings: list[list[int]]) -> int:
```

## Constraints

- `0 <= len(meetings) <= 10**5`
- `0 <= start < end <= 10**9`

## Examples

**Example 1**

```
Input:  meetings = [[0, 10], [2, 4], [6, 8], [3, 7]]
Output: 3
```

**Example 2**

```
Input:  meetings = [[1, 2], [2, 3]]
Output: 1
```

## Run

```
python judge.py 27
```
