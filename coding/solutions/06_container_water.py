def max_area(heights):
    i, j = 0, len(heights) - 1
    best = 0
    while i < j:
        best = max(best, min(heights[i], heights[j]) * (j - i))
        if heights[i] < heights[j]:
            i += 1
        else:
            j -= 1
    return best


def brute(heights):
    n = len(heights)
    return max(min(heights[i], heights[j]) * (j - i) for i in range(n) for j in range(i + 1, n))
