def almost_palindrome(s):
    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return is_pal(i + 1, j) or is_pal(i, j - 1)
        i += 1
        j -= 1
    return True


def brute(s):
    if s == s[::-1]:
        return True
    for k in range(len(s)):
        t = s[:k] + s[k + 1:]
        if t == t[::-1]:
            return True
    return False
