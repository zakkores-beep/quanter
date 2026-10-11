from lib import build_list, list_values


def reverse_list(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


def brute(head):
    return build_list(list_values(head)[::-1])
