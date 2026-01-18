# Problem: Level Order Traversal
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(n) 

# Input:  
#    3
#   / \
#  9  20
#    / \
#  15  7
# Output: 
# [
#   [3],
#   [9, 20],
#   [15, 7]
# ]

# Brute force idea : 
# A brute-force approach would first compute the height of the tree.
# Then, for each level from 0 to height − 1, I would traverse the entire tree and 
# collect all nodes that belong to that level.
# This requires repeatedly scanning the tree for every level, which is inefficient.

# Optimisation
# Pattern: BFS 

# Key idea: I use a queue to perform a breadth-first traversal of the tree.
# I first add the root node to the queue.
# While the queue is not empty, I process nodes level by level by first storing the current size of the queue, 
# which represents the number of nodes at that level.
# I then dequeue exactly that many nodes, add their values to a list for the current level, 
# and enqueue their left and right children if they exist.
# After processing all nodes at that level, I append the level list to the result.
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(3)
node9 = TreeNode(9)
node20 = TreeNode(20)
node15 = TreeNode(15)
node7 = TreeNode(7)

# Link nodes
root.left = node9
root.right = node20
node20.left = node15
node20.right = node7

def levelOrderTraversal(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


print(levelOrderTraversal(root))