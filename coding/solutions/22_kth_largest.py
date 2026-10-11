import heapq


def kth_largest(fills, k):
    heap = []
    for x in fills:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]


def brute(fills, k):
    return sorted(fills, reverse=True)[k - 1]
