# Problem: Two Sum
# Time complexity: O(n)
# Space complexity: O(n)

# Input: 
# nums = [2, 7, 11, 15]
# target = 9
# Output:
# [0, 1]

# Brute force idea : 
# 1. run an outer loop till the length of nums using i as a variable
# 2. run and inner loop from i+1 till the end of nums using j as a variable
# 3. add nums[i] and nums[j] and if it matches the target, return i and j as [i, j]

# Optimisation
# Pattern: Hashmap
# Key idea: Using lookup on hashmap storing values against their indices to check whether the difference between a certain number in the array exists in the dictionary keys, if so, return the current index and the index of the corresponding difference from the dictionary value
def main(nums, target):
    if len(nums)<2:
        return []
    seen = {}
    for i in range(len(nums)):
        if(target - nums[i] in seen):
            return([seen[target-nums[i]], i])
        seen[nums[i]] = i
print(main([3,3], 6))