# 12. Colliding Orders

**Difficulty:** medium · **Topic:** stack

Objects sit on a line in the given order. For `orders[i]`, the absolute value
is its size and the sign is its direction (positive = moving right, negative =
moving left). All move at the same speed.

When two objects meet, the smaller one disappears; if they are the same size,
both disappear. Objects moving in the same direction never meet. Return the
objects that remain, in their original order.

## Function

```python
def surviving(orders: list[int]) -> list[int]:
```

## Constraints

- `0 <= len(orders) <= 2 * 10**5`
- `1 <= abs(orders[i]) <= 1000` (no zeros)

## Examples

**Example 1**

```
Input:  orders = [10, 2, -5]
Output: [10]
```

**Example 2**

```
Input:  orders = [-2, 1]
Output: [-2, 1]
```

**Example 3**

```
Input:  orders = [5, -5]
Output: []
```

## Run

```
python judge.py 12
```
