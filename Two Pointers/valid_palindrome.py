# Problem: Valid Palindrome
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(1)

# Input: 
# s = "A man, a plan, a canal: Panama"
# Output: 
# True

# Brute force idea: 
# Traverse the string and build a new string containing only alphanumeric 
# characters, converting all letters to the same case (lowercase or uppercase). 
# Reverse this s string. Compare the s string with its reversed version. 
# If both are identical, the string is a palindrome; otherwise, it is not.

# Optimisation
# Pattern: Two Pointers
# Key idea:
#Use two pointers starting from the beginning and end of the string. 
# Move inward while comparing characters, ignoring non-alphanumeric characters and case differences. 
# If all valid character pairs match, the string is a palindrome. 
# How pointers move Left pointer starts at index 0, right pointer at n - 1 
# If both characters are alphanumeric, compare them and move both pointers inward 
# If a mismatch occurs, return False How non-alphanumeric characters are handled 
# If the left character is non-alphanumeric, move the left pointer forward 
# If the right character is non-alphanumeric, move the right pointer backward 
# These characters are skipped and never compared

def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True

print(isPalindrome("A man, a plan, a canal: Panama"))