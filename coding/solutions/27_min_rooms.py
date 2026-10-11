import heapq


def min_rooms(meetings):
    ends = []  # end times of rooms in use
    for s, e in sorted(meetings):
        if ends and ends[0] <= s:
            heapq.heapreplace(ends, e)
        else:
            heapq.heappush(ends, e)
    return len(ends)


def brute(meetings):
    """The peak overlap happens at some meeting's start time."""
    return max([sum(1 for s, e in meetings if s <= t < e) for t, _ in meetings], default=0)
