# Problem: Diameter of Binary Tree
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(h) [h: height of tree (balanced tree - O(log n), skewed tree - O(n))]

# Input:
#         1
#        / \
#       2   3
#      / \
#     4   5

# Output: 3

# Brute force idea : 
# A brute-force approach would consider every node as a potential starting point.
# For each node, I would compute the longest path to all other nodes (for example, by calculating depths or distances), 
# and keep track of the maximum number of edges found between any two nodes.
# This results in repeatedly recomputing depths for many nodes, making the approach inefficient.
    
# Optimisation
# Pattern: DFS (Postorder)

# Key idea: I use a postorder DFS where each recursive call returns the height of the subtree rooted at that node.
# At each node, I compute the height of the left and right subtrees.
# The diameter passing through the current node is the sum of the left and right subtree heights, and I update a global maximum diameter with this value.
# Finally, the recursive call returns 1 + max(left_height, right_height) so parent nodes can compute their own diameters.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Create nodes
root = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)

# Link nodes
root.right = node3
root.left = node2
node2.right = node5
node2.left = node4


def diameterOfBinaryTree(root):
    diameter = 0

    def dfs(node):
        nonlocal diameter
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        diameter = max(diameter, left + right)

        return 1 + max(left, right)

    dfs(root)
    return diameter


print(diameterOfBinaryTree(root))  