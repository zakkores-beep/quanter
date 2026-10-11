# 28. Unlimited Round Trips

**Difficulty:** easy · **Topic:** greedy

`prices[i]` is a stock's price on day `i`. You may buy and sell as many
times as you like, but you can hold at most one share at a time (sell
before buying again). Buying and selling happen at that day's price.
Return the maximum total profit (0 if you never trade).

## Function

```python
def max_profit(prices: list[int]) -> int:
```

## Constraints

- `1 <= len(prices) <= 2 * 10**5`
- `0 <= prices[i] <= 10**4`

## Examples

**Example 1**

```
Input:  prices = [1, 5, 3, 6, 4]
Output: 7
```

**Example 2**

```
Input:  prices = [5, 4, 3]
Output: 0
```

## Run

```
python judge.py 28
```
