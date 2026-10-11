# 2. Longest Active Streak

**Difficulty:** medium · **Topic:** arrays & hashing

`days` holds the (unsorted) day numbers on which an account traded. A day can
appear more than once. Return the length of the longest run of consecutive
integers `x, x+1, ..., x+L-1` that all appear in `days`. Return 0 for an
empty list.

Aim for O(n) time; sorting works but is not the intended solution.

## Function

```python
def longest_streak(days: list[int]) -> int:
```

## Constraints

- `0 <= len(days) <= 2 * 10**5`
- `-10**9 <= days[i] <= 10**9`

## Examples

**Example 1**

```
Input:  days = [10, 5, 6, 100, 4, 7]
Output: 4
```

**Example 2**

```
Input:  days = [1, 2, 2, 3, 9]
Output: 3
```

## Run

```
python judge.py 2
```
