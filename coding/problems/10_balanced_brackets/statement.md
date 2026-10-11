# 10. Balanced Brackets

**Difficulty:** easy · **Topic:** stack

`s` contains only the characters `()[]{}`. Return `True` if every opening
bracket is closed by the same type of bracket in the correct order, otherwise
`False`. The empty string is balanced.

## Function

```python
def is_balanced(s: str) -> bool:
```

## Constraints

- `0 <= len(s) <= 2 * 10**5`

## Examples

**Example 1**

```
Input:  s = '{[]}()'
Output: True
```

**Example 2**

```
Input:  s = '([)]'
Output: False
```

## Run

```
python judge.py 10
```
