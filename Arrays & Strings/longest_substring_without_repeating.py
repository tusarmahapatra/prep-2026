# Problem: Longest substring without repeating characters
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(n)

# Input: "abcabcbb"
# Output: 3

# Brute force idea : 
# I generate all possible substrings using two nested loops.
# For each substring, I check whether it contains duplicate characters using a set or frequency array.
# If the substring has all unique characters, I update the maximum length.
# Finally, I return the maximum length found.

# Optimisation
# Pattern: Sliding window
# Key idea: I use a sliding window with two pointers representing a substring with all unique characters.
# I maintain a set to track characters inside the window.
# I expand the window by moving the right pointer.
# If a duplicate character is found, I shrink the window from the left until the duplicate is removed.
# At each step, I update the maximum window length.

def lengthOfLongestSubstring(self, s: str) -> int:
    seen = set()
    i = 0
    max_length = 0

    for j, c in enumerate(s):
        while c in seen:
            seen.remove(s[i])
            i += 1
        seen.add(c)
        max_length = max(max_length, j - i + 1)
    return max_length
print(lengthOfLongestSubstring("abcabcbb"))