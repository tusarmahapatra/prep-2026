# Problem: Detect Cycle
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(1)

# Input:  1 → 2 → 3 → 4 → 5->None
# Output: False

# Brute force idea : 
# I traverse the linked list while storing each visited node reference in a hash set.
# If at any point I encounter a node that already exists in the set, a cycle is present.
# If traversal reaches None, then no cycle exists.

# Optimisation
# Pattern: Fast and Slow pointers

# Key idea: I use two pointers, slow and fast, both starting at the head of the linked list.
# In each iteration, slow moves one step and fast moves two steps.
# If the linked list contains a cycle, the fast pointer will eventually catch up to the slow pointer, and they will point to the same node.
# If the fast pointer reaches None, it means the list terminates and no cycle exists.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
# Create nodes
head = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)

# Link nodes
head.next = node2
node2.next = node3
node3.next = node2 

def hasCycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
print(hasCycle(head))
