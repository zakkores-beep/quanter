# 11. Days Until a Higher Price

**Difficulty:** medium · **Topic:** stack

For each day `i`, return how many days you must wait until a **strictly
higher** price than `prices[i]`. Use 0 if no later day has a higher price.

## Function

```python
def days_until_higher(prices: list[int]) -> list[int]:
```

## Constraints

- `1 <= len(prices) <= 2 * 10**5`
- `1 <= prices[i] <= 10**6`

## Examples

**Example 1**

```
Input:  prices = [73, 71, 75, 70, 76, 72]
Output: [2, 1, 2, 1, 0, 0]
```

**Example 2**

```
Input:  prices = [3, 3, 3]
Output: [0, 0, 0]
```

## Run

```
python judge.py 11
```
