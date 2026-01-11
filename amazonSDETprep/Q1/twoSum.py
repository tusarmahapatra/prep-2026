def twoSum( nums, target):
    seen = {}
    for i in range(len(nums)):
        if target-nums[i] in seen.keys():
            return([seen[target-nums[i]], i] )
        seen[nums[i]] = i
        
        
  

    #return [seen[target-nums[i]], i]
    
nums = [11,2,7,15]
target = 9
print(twoSum( nums, target))
