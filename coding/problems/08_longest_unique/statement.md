# 8. Longest Run Without Repeats

**Difficulty:** medium · **Topic:** sliding window

Return the length of the longest substring (contiguous) of `s` in which no
character appears twice.

## Function

```python
def longest_unique(s: str) -> int:
```

## Constraints

- `0 <= len(s) <= 2 * 10**5`
- `s` contains lowercase letters and digits

## Examples

**Example 1**

```
Input:  s = 'xyzxyzz'
Output: 3
```

**Example 2**

```
Input:  s = 'abba'
Output: 2
```

## Run

```
python judge.py 8
```
