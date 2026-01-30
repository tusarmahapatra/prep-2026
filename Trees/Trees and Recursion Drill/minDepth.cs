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
    public int MinDepth(TreeNode root)
    {
        if (root == null)
            return 0;

        int left = MinDepth(root.left);
        int right = MinDepth(root.right);

        // Special case: one subtree is null
        if (left == 0)
            return 1 + right;

        if (right == 0)
            return 1 + left;

        return 1 + Math.Min(left, right);
    }
}