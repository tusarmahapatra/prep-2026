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
    public IList<int> PostorderTraversal(TreeNode root)
    {
        // This list will store the postorder traversal result
        List<int> result = new List<int>();

        // Call the recursive helper function
        DFS(root, result);

        // Return the result
        return result;
    }

    private void DFS(TreeNode node, List<int> result)
    {
        if(node == null){
            return;
        }
        
        DFS(node.left, result);
        DFS(node.right, result);
        result.Add(node.val);
        
        
    }
}
