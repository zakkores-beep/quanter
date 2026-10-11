def surviving(orders):
    stack = []
    for x in orders:
        alive = True
        while alive and x < 0 and stack and stack[-1] > 0:
            if stack[-1] < -x:
                stack.pop()
            elif stack[-1] == -x:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(x)
    return stack


def brute(orders):
    """Repeatedly resolve the first adjacent right-mover/left-mover pair."""
    a = list(orders)
    while True:
        for i in range(len(a) - 1):
            if a[i] > 0 and a[i + 1] < 0:
                left, right = a[i], -a[i + 1]
                if left > right:
                    del a[i + 1]
                elif left < right:
                    del a[i]
                else:
                    del a[i:i + 2]
                break
        else:
            return a
