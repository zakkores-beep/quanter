import heapq


def merge_feeds(feeds):
    heap = [(f[0], i, 0) for i, f in enumerate(feeds) if f]
    heapq.heapify(heap)
    out = []
    while heap:
        val, i, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(feeds[i]):
            heapq.heappush(heap, (feeds[i][j + 1], i, j + 1))
    return out


def brute(feeds):
    return sorted(x for f in feeds for x in f)
