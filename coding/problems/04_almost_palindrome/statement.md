# 4. Almost a Palindrome

**Difficulty:** easy · **Topic:** two pointers

Return `True` if `s` reads the same forwards and backwards after deleting
**at most one** character, otherwise `False`.

## Function

```python
def almost_palindrome(s: str) -> bool:
```

## Constraints

- `1 <= len(s) <= 2 * 10**5`
- `s` contains only lowercase English letters

## Examples

**Example 1**

```
Input:  s = 'abca'
Output: True
```

**Example 2**

```
Input:  s = 'abc'
Output: False
```

**Example 3**

```
Input:  s = 'racecar'
Output: True
```

## Run

```
python judge.py 4
```
