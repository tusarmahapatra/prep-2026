def isValid(s):
    col = []
    s = "()[]{}"
    for i in s:
        stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for ch in s:
        if ch in mapping.values():
            stack.append(ch)
        else:
            if not stack:
                return False
            if stack.pop() != mapping[ch]:
                return False

    return len(stack) == 0