from lib import build_list, list_values


def reorder(head):
    if not head or not head.next:
        return head
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next
    first, second = head, prev
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next, second.next = second, nxt1
        first, second = nxt1, nxt2
    return head


def brute(head):
    vals = list_values(head)
    out, i, j = [], 0, len(vals) - 1
    while i <= j:
        out.append(vals[i])
        if i != j:
            out.append(vals[j])
        i += 1
        j -= 1
    return build_list(out)
