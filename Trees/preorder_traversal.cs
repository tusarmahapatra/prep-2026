using System;
using System.Collections.Generic;

public class TreeNode
{
    public int val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(int val = 0, TreeNode left = null, TreeNode right = null)
    {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

public class Solution
{
    public IList<int> PreorderTraversal(TreeNode root)
    {
        // This list will store the preorder traversal result
        List<int> result = new List<int>();

        // Call the recursive helper function
        DFS(root, result);

        // Return the result
        return result;
    }

    private void DFS(TreeNode node, List<int> result)
    {
        // 1️⃣ Base case: if node is null, stop recursion
        // TODO
        if(node == null){
            return;
        }
        // 2️⃣ Process the current node (preorder = root first)
        // TODO
        result.Add(node.val);
        // 3️⃣ Recursively traverse the left subtree
        // TODO
        DFS(node.left, result);
        // 4️⃣ Recursively traverse the right subtree
        // TODO
        DFS(node.right, result);
    }
}
