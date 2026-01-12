# Problem: Subarray sum equals k
# Difficulty: Medium
# Time complexity: O(n)
# Space complexity: O(n)

# Input: 
# nums = [1,1,1]
# k = 2
# Output:
# 2

# Brute force idea : 
# I use two nested loops.
# The outer loop fixes the starting index of the subarray.
# The inner loop extends the subarray to the right while maintaining a running sum.
# For each extension, if the running sum equals k, I increment a counter.
# I repeat this for all possible starting indices.

# Optimisation
# Pattern: Hashmap
# Key idea: I use a running prefix sum while iterating through the array.
# I maintain a hashmap that stores how many times each prefix sum has occurred.
# At each index, if current_sum - k exists in the hashmap, it means there are that many subarrays 
# ending at the current index whose sum equals k.
# I add this count to the result, then update the hashmap with the current prefix sum.
# I initialize the hashmap with {0: 1} to handle subarrays that start at index 0.
def subarray_sum_equals_k(nums, k):
    prefix_sums = {0: 1}
    count = 0
    prefix_sum = 0
    for i, c in enumerate(nums):
        prefix_sum += c
        if prefix_sum - k in prefix_sums:
            count += prefix_sums[prefix_sum-k]
        prefix_sums[prefix_sum] = prefix_sums.get(prefix_sum, 0)+1
    return count
print(subarray_sum_equals_k([3,3], 6))
