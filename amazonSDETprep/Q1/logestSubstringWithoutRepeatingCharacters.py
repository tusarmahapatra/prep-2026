# Input: s = "abcabcbb"
# Output: 3
# Explanation: "abc"
def lengthOfLongestSubstring(s):
    max_length = 0
    left = 0
    seen = set()
    for right, c in enumerate(s):
        while c in seen:
            seen.remove(s[left ])
            left+=1
        seen.add(c)
        max_length = max_length if max_length>right-left+1 else right-left+1
    return max_length
        
print(lengthOfLongestSubstring('abcabcbb'))