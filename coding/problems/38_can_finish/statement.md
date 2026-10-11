# 38. Dependency Order

**Difficulty:** medium · **Topic:** graphs

There are `n` jobs labelled `0 .. n-1`. Each pair `[a, b]` in `deps` means
job `b` must run before job `a`. Return `True` if all jobs can be run in
some order, i.e. the dependencies contain no cycle. (`[a, a]` is a cycle.)

## Function

```python
def can_finish(n: int, deps: list[list[int]]) -> bool:
```

## Constraints

- `1 <= n <= 10**5`
- `0 <= len(deps) <= 2 * 10**5`
- `0 <= a, b < n`; duplicate pairs may appear

## Examples

**Example 1**

```
Input:  n = 2, deps = [[1, 0]]
Output: True
```

**Example 2**

```
Input:  n = 3, deps = [[1, 0], [2, 1], [0, 2]]
Output: False
```

## Run

```
python judge.py 38
```
