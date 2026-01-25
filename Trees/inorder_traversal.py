# Problem: Inorder Traversal
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(h) [h: height of tree (balanced tree - O(log n), skewed tree - O(n))]

# Input:  
# 1
#  \
#   2
#  /
# 3
# Output: [1, 3, 2]

# Brute force idea : 
# A brute-force approach would try to manually simulate inorder traversal by repeatedly navigating to the leftmost node, keeping track of parent nodes, and then backtracking to visit right subtrees.
# This requires explicitly managing traversal state and becomes complex and error-prone without a clear structure like recursion or a stack.

# Optimisation
# Pattern: DFS 

# Key idea: I use a recursive DFS approach.
# The base case is when the current node is None, in which case I return.
# For each node, I first recursively traverse the left subtree, then process the current node, and finally recursively traverse the right subtree.
# This left → root → right order naturally produces the inorder traversal.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Create nodes
root = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)

# Link nodes
root.right = node2
node2.left = node3

def inorderTraversal(root):
    result = []
    def dfs(root):
        if root == None:
            return 
        dfs(root.left)
        result.append(root.val)
        dfs(root.right)
    dfs(root)
    return result


print(inorderTraversal(root))  # [1, 3, 2]