# 24. Merge Sorted Order Feeds

**Difficulty:** medium · **Topic:** heaps

Each feed is a list of timestamps sorted in non-decreasing order. Merge all
feeds into one sorted list.

Use a heap holding one "next" element per feed: O(N log k) for N total
items and k feeds.

## Function

```python
def merge_feeds(feeds: list[list[int]]) -> list[int]:
```

## Constraints

- `0 <= len(feeds) <= 2000`
- total items `N <= 2 * 10**5`
- `-10**9 <= timestamp <= 10**9`

## Examples

**Example 1**

```
Input:  feeds = [[1, 5, 9], [2, 2], [0, 10]]
Output: [0, 1, 2, 2, 5, 9, 10]
```

**Example 2**

```
Input:  feeds = [[], [3], []]
Output: [3]
```

## Run

```
python judge.py 24
```
