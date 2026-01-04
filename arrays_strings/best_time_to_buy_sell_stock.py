# Problem: Best time to Buy or Sell stock
# Time complexity: O(n)
# Space complexity: O(1)

# Input: 
# prices = [7, 1, 5, 3, 6, 4]
# Output:
# 5

# Brute force idea : O(n^2) time complexity
# 1. hold a variable - max_profit and initialise it to 0
# 2. iterate through the prices array using i as a variable and also iterate through the same array from i+1 using j as a variable
# 3. set value of max_profit as max(max_profit, prices[j]-prices[i]) 
# 4. return max_profit at the end of the loops

# Optimisation
# Pattern: Prefix Minimum / Running Minimum /State Tracking ?One pass optimisation
# Key idea: for updating the maxProfit in one pass, maxProfit is initialised to 0, and its value is set to prices[i]-minBuy minBuy is another variable initialised with prices[i] and set to min(minBuy, prices[i]) while iteration
def main(prices):
    minBuy = prices[0]
    maxProfit = 0

    for price in prices:
        maxProfit = max(maxProfit, price - minBuy)
        minBuy = min(minBuy, price)

    return maxProfit
print(main([7, 1, 5, 3, 6, 4]))