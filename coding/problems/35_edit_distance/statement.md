# 35. Ticker Edit Distance

**Difficulty:** medium · **Topic:** 2-D dynamic programming

Return the minimum number of single-character edits (insert a character,
delete a character, or replace a character) that turn `a` into `b`.

## Function

```python
def edit_distance(a: str, b: str) -> int:
```

## Constraints

- `0 <= len(a), len(b) <= 500`
- lowercase letters only

## Examples

**Example 1**

```
Input:  a = 'spread', b = 'bread'
Output: 2
```

**Example 2**

```
Input:  a = 'trade', b = 'trader'
Output: 1
```

## Run

```
python judge.py 35
```
