# Problem: Valid parentheses
# Difficulty: Medium
# Time complexity: O(n)
# Space complexity: O(n)

# Input:  [73, 74, 75, 71, 69, 72, 76, 73]
# Output: [1, 1, 4, 2, 1, 1, 0, 0]

# Brute force idea : 
# For each day, I iterate over all future days until I find a day with a higher temperature.
# I count how many days it takes to find a warmer temperature.
# If no warmer day exists, I store 0.

# Optimisation
# Pattern: Monotonic Stack (Decreasing)
# Key idea: I use a monotonic decreasing stack that stores indices of days whose next warmer temperature has not been found yet.
# As I iterate through the temperature array, if the current temperature is higher than the temperature 
# at the index on top of the stack, it means I have found the next warmer day for that index.
# I pop the index from the stack and compute the number of days waited as the difference between the current index and the popped index.
# This process continues until the stack is empty or the monotonic decreasing order is restored.
# Finally, I push the current index onto the stack.
def daily_temperatures(temperatures):
    stack = []
    res = [0] * len(temperatures)
    for current_day, temp in enumerate(temperatures):
        while stack and temp > temperatures[stack[-1]]:
            prev_day = stack.pop()
            res[prev_day] = current_day - prev_day
            
        stack.append(current_day)
    return res


print(daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]))