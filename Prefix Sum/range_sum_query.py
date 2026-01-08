# Problem: Range sum query
# Difficulty: Easy
# Time complexity: O(n+q)
# Space complexity: O(n)

# Input
# ["NumArray", "sumRange", "sumRange", "sumRange"]
# [[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
# Output
# [ 1, -1, -3]

# Brute force idea : 
# For each query, I iterate from index left to right and add all the elements in that range.
# I repeat this process independently for every query.

# Optimisation
# Pattern: Prefix Sum
# Key idea: I precompute a prefix sum array where each index stores the sum from index 0 to that position.
# To answer a query [left, right], if left is zero I return prefix[right], otherwise I return prefix[right] - prefix[left - 1].
# This allows each query to be answered in O(1) time.

class NumArray:
    def __init__(self, nums):
        self.prefix = [0] * len(nums)
        if nums:
            self.prefix[0] = nums[0]
            for i in range(1, len(nums)):
                self.prefix[i] = self.prefix[i - 1] + nums[i]

    def sumRange(self, left, right):
        if left == 0:
            return self.prefix[right]
        return self.prefix[right] - self.prefix[left - 1]