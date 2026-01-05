# Problem: Two Sum II
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(1)

# Input:
# numbers = [2, 7, 11, 15]
# target = 9

# Output:
# [1, 2]

# Brute force idea: 
# Traverse the array using nested loops using i for the outer loop and j for the inner loop(j starts from i+1) if at any point, array of i + array of j equal target, return [i,j]

# Optimisation
# Pattern: Two Pointers
# Key idea:
# I use two pointers: one at the start and one at the end of the sorted array.
# I compute the sum of the two values.
# If the sum is smaller than the target, I move the left pointer rightward to increase the sum.
# If the sum is larger than the target, I move the right pointer leftward to decrease the sum.
# When the sum equals the target, I return the indices (1-based).

def twoSum2(nums, target) :
    left, right = 0, len(nums) - 1

    while left < right:
        if nums[left]+nums[right]>target:
            right-=1
        if nums[left]+nums[right]<target:
            left+=1
        if nums[left]+nums[right]==target:
            return [left+1, right+1]
    

print(twoSum2([2, 7, 11, 15], 9))