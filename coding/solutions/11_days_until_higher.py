def days_until_higher(prices):
    ans = [0] * len(prices)
    stack = []  # indices with no higher price found yet; prices decreasing
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] < p:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans


def brute(prices):
    n = len(prices)
    ans = []
    for i in range(n):
        wait = 0
        for j in range(i + 1, n):
            if prices[j] > prices[i]:
                wait = j - i
                break
        ans.append(wait)
    return ans
