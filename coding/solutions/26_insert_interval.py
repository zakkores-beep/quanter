def insert_interval(intervals, new):
    s, e = new
    out, i, n = [], 0, len(intervals)
    while i < n and intervals[i][1] < s:
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= e:
        s, e = min(s, intervals[i][0]), max(e, intervals[i][1])
        i += 1
    out.append([s, e])
    out.extend(intervals[i:])
    return out


def brute(intervals, new):
    """Append, then merge any two overlapping intervals until none overlap."""
    items = [list(x) for x in intervals] + [list(new)]
    merged = True
    while merged:
        merged = False
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, b = items[i], items[j]
                if a[0] <= b[1] and b[0] <= a[1]:
                    items[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    del items[j]
                    merged = True
                    break
            if merged:
                break
    return sorted(items)
