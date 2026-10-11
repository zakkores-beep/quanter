from itertools import combinations


def count_zero_triplets(nums):
    a = sorted(nums)
    n = len(a)
    count = 0
    for i in range(n - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = a[i] + a[lo] + a[hi]
            if s < 0:
                lo += 1
            elif s > 0:
                hi -= 1
            else:
                count += 1
                v = a[lo]
                while lo < hi and a[lo] == v:
                    lo += 1
    return count


def brute(nums):
    return len({tuple(sorted(c)) for c in combinations(nums, 3) if sum(c) == 0})
