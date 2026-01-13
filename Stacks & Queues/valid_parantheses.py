# Problem: Valid parentheses
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(n)

# Input: "()[]{}"
# Output: True

# Brute force idea : 
# A brute-force approach could try to repeatedly remove matching pairs like (), {}, and [] from the string until no more removals are possible.
# However, this approach is inefficient and error-prone because it requires repeated scans of the string and does not naturally handle nested or ordered dependencies

# Optimisation
# Pattern: Stack
# Key idea: I iterate through the string character by character.
# Whenever I encounter an opening bracket, I push it onto the stack.
# When I encounter a closing bracket, I check whether the stack is empty or the top of the stack does not match the corresponding opening bracket—if so, the string is invalid.
# If it matches, I pop the opening bracket from the stack.
# After processing the entire string, if the stack is empty, the string is valid; otherwise, it is invalid.
def valid_parentheses(s):
    stack = []
    for c in s:
        if c in ['(', '{', '[']:
            stack.append(c)
        if c == ')':
            if stack and stack[-1] == '(':
                stack.pop()
            else:
                return False
        if c == '}':
            if stack and stack[-1] == '{':
                stack.pop()
            else:
                return False
        if c == ']':
            if stack and stack[-1] == '[':
                stack.pop()
            else:
                return False
    if len(stack)==0:
        return True
    return False
print(valid_parentheses("("))