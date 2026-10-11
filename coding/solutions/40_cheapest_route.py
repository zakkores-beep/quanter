import heapq


def cheapest_route(n, fees, src, dst):
    adj = [[] for _ in range(n)]
    for u, v, f in fees:
        adj[u].append((v, f))
    dist = [None] * n
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] is not None:
            continue
        dist[u] = d
        if u == dst:
            return d
        for v, f in adj[u]:
            if dist[v] is None:
                heapq.heappush(heap, (d + f, v))
    return -1


def brute(n, fees, src, dst):
    """Bellman-Ford: relax every edge n - 1 times."""
    inf = float("inf")
    dist = [inf] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, f in fees:
            if dist[u] + f < dist[v]:
                dist[v] = dist[u] + f
    return -1 if dist[dst] == inf else dist[dst]
