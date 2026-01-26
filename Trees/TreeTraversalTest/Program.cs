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
        List<int> result = new List<int>();
        DFS(root, result);
        return result;
    }

    private void DFS(TreeNode node, List<int> result)
    {
        if (node == null)
            return;

        result.Add(node.val);
        DFS(node.left, result);
        DFS(node.right, result);
    }
}

class Program
{
    static void Main()
    {
        // Build test tree:
        //        1
        //         \
        //          2
        //         /
        //        3

        TreeNode root = new TreeNode(1);
        root.right = new TreeNode(2);
        root.right.left = new TreeNode(3);

        Solution sol = new Solution();
        IList<int> result = sol.PreorderTraversal(root);

        Console.WriteLine(string.Join(", ", result));
    }
}
