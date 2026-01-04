# Problem: Contains duplicates
# Time complexity: O(n)
# Space complexity: O(n)

# Input: 
# nums = [1,2,3,1]
# Output:
# True

# Brute force idea : O(n^2) time complexity
# running a nested loop and checking each number in the inner loop with each number in the outerloop

# Optimisation
# Pattern: Hashset
# Key idea: Iterate through the array and store each number in a hash set.
# Before inserting a number, check if it already exists in the set.
# If it does, return true immediately.
# If the loop finishes, return false.
def main(a):
    seen = set()
    for i in a:
        if i in seen:
            return True
        seen.add(i)
    return False
print(main([1,2,3,1]))