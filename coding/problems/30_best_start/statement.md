# 30. Circular Funding Route

**Difficulty:** medium · **Topic:** greedy

There are `n` stations on a circle. At station `i` you collect `gas[i]`, and
travelling from station `i` to station `(i + 1) % n` uses `cost[i]`. You
start with an empty tank at a station of your choice and must go once round
the whole circle; the tank may never go negative.

Return the **smallest** starting index that works, or -1 if none does.

## Function

```python
def best_start(gas: list[int], cost: list[int]) -> int:
```

## Constraints

- `1 <= n == len(gas) == len(cost) <= 2 * 10**5`
- `0 <= gas[i], cost[i] <= 10**4`

## Examples

**Example 1**

```
Input:  gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2]
Output: 3
```

**Example 2**

```
Input:  gas = [1, 1], cost = [1, 1]
Output: 0
```

## Run

```
python judge.py 30
```
