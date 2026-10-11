from lib import ListNode, build_list, list_values


def merge_lists(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def brute(a, b):
    return build_list(sorted(list_values(a) + list_values(b)))
