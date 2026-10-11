# 36. Longest Common Subsequence

**Difficulty:** medium · **Topic:** 2-D dynamic programming

Return the length of the longest string that is a subsequence of both `a`
and `b` (characters keep their order but need not be adjacent).

## Function

```python
def common_subsequence(a: str, b: str) -> int:
```

## Constraints

- `0 <= len(a), len(b) <= 500`
- lowercase letters only

## Examples

**Example 1**

```
Input:  a = 'market', b = 'marker'
Output: 5
```

**Example 2**

```
Input:  a = 'abc', b = 'def'
Output: 0
```

## Run

```
python judge.py 36
```
