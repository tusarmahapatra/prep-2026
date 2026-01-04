# Problem: Valid anagram
# Time complexity: O(n)
# Space complexity: O(n)

# Input: 
# s = "anagram"
# t = "nagaram"
# Output:
# True

# Brute force idea:
# For each character, count its occurrences in both strings using nested loops.
# If any count differs, return False.

# Optimisation
# Pattern: Hashmap
# Key idea: I use two hash maps to count the frequency of each character in both strings.
# If the two maps are equal, the strings are anagrams; otherwise, they are not.
def main(s, t):
    if len(s)!= len(t):
        return False
    s_ = {}
    t_ = {}
    for i in range(len(s)):
        if(s[i] not in s_):
            s_[s[i]] = 1
        else:
            s_[s[i]] += 1
        if(t[i] not in t_):
            t_[t[i]] = 1
        else:
            t_[t[i]] += 1
    return s_ == t_
print(main("anagram", "nagaram"))