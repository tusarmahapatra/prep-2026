# Problem: Contains duplicates
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(n)

# Input:
# nums = [1,2,3,1]
# Output:
# True

# Brute force idea : O(n^2) time complexity
# running a nested loop and checking each number in the inner loop with each number in the outer loop

# Optimisation
# Pattern: HashSet
# Key idea:
# Iterate through the array and store each number in a hash set.
# Before inserting a number, check if it already exists in the set.
# If it does, return True immediately.
# If the loop finishes, return False.

def main(nums):
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False


# Example usage
if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    print(main(nums))  # Output: True
