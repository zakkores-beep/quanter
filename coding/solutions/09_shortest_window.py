def shortest_window(volumes, target):
    best = float("inf")
    total = left = 0
    for right, v in enumerate(volumes):
        total += v
        while total >= target:
            best = min(best, right - left + 1)
            total -= volumes[left]
            left += 1
    return 0 if best == float("inf") else best


def brute(volumes, target):
    n = len(volumes)
    best = 0
    for i in range(n):
        for j in range(i, n):
            if sum(volumes[i:j + 1]) >= target:
                if best == 0 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best
