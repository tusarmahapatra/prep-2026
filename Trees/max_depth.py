# Problem: Max Depth
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(h) [h: height of tree (balanced tree - O(log n), skewed tree - O(n))]

# Input:
#       3
#      / \
#     9  20
#        / \
#       15  7

# Output: 3

# Brute force idea : 
# A brute-force approach would explore all root-to-leaf paths using DFS.
# For each path, I would keep track of the current depth using a counter.
# When a leaf node is reached, I compare the current depth with a global maximum depth and update it if needed.
# After exploring all paths, I return the maximum depth found.

# Optimisation
# Pattern: DFS 

# Key idea: I use a recursive DFS where each function call returns the maximum depth of the subtree rooted at that node.
# For a given node, I recursively compute the depth of its left and right subtrees.
# The depth at the current node is 1 + max(left_depth, right_depth).
# This bottom-up computation naturally fits a postorder traversal.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Create nodes
root = TreeNode(3)
node2 = TreeNode(9)
node3 = TreeNode(20)
node4 = TreeNode(15)
node5 = TreeNode(7)

# Link nodes
root.right = node3
root.left = node2
node3.right = node5
node3.left = node4


def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))


print(maxDepth(root))  