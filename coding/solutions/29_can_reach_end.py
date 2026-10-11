def can_reach_end(jumps):
    reach = 0
    for i, j in enumerate(jumps):
        if i > reach:
            return False
        reach = max(reach, i + j)
    return True


def brute(jumps):
    n = len(jumps)
    ok = [False] * n
    ok[0] = True
    for i in range(n):
        if ok[i]:
            for step in range(1, jumps[i] + 1):
                if i + step < n:
                    ok[i + step] = True
    return ok[-1]
