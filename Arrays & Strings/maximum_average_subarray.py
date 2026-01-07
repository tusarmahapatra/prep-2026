# Problem: Maximum average subarray
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(1)

# Input:
# nums = [1,12,-5,-6,50,3]
# k = 4

# Output:
# 12.75

# Brute force idea : 
# I use a loop that starts each subarray at index i.
# For each i, I use an inner loop to sum the next k elements from i to i + k - 1.
# I compute the average of these k elements and keep track of the maximum average seen so far.
# Finally, I return the maximum average.

# Optimisation
# Pattern: Sliding window
# Key idea: I use a fixed-size sliding window of length k.
# I first compute the sum of the first k elements.
# Then I slide the window one element at a time by adding the next element and removing the element that leaves the window.
# At each step, I update the maximum average using the current window sum divided by k.

def maxAvgSubarray(nums, k):
    # Sum of first window
    window_sum = sum(nums[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(nums)):
        window_sum += nums[i]       # add new element
        window_sum -= nums[i - k]   # remove old element
        max_sum = max(max_sum, window_sum)

    return max_sum / k
print(maxAvgSubarray([1,12,-5,-6,50,3], 4))