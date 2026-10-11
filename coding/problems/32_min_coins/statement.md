# 32. Fewest Lots

**Difficulty:** medium · **Topic:** 1-D dynamic programming

You can buy any number of each lot size in `lots`. Return the fewest lots
whose sizes add up to exactly `amount`, or -1 if that is impossible.
`amount = 0` needs 0 lots.

Greedy (always take the biggest lot) is **wrong** in general.

## Function

```python
def min_coins(lots: list[int], amount: int) -> int:
```

## Constraints

- `1 <= len(lots) <= 12`, sizes distinct
- `1 <= lots[i] <= 10**4`
- `0 <= amount <= 10**4`

## Examples

**Example 1**

```
Input:  lots = [1, 3, 4], amount = 6
Output: 2
```

**Example 2**

```
Input:  lots = [2], amount = 3
Output: -1
```

## Run

```
python judge.py 32
```
