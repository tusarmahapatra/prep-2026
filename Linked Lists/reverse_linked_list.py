# Problem: Linked List Reversal
# Difficulty: Easy
# Time complexity: O(n)
# Space complexity: O(1)

# Input:  1 → 2 → 3 → 4 → 5
# Output: 5 → 4 → 3 → 2 → 1

# Brute force idea : 
# I traverse the linked list and store all node values in an auxiliary array.
# Then I traverse the list again and overwrite the node values in reverse order using the array.
# This reverses the list but uses extra space.

# Optimisation
# Pattern: In-place Pointer Reversal
# Key idea: Reverse the link of each node, starting from the head and moving towards the 
# tail of the linked list. Take three-pointers, ‘curr’, ‘ahead’, ‘prev’. Initialize curr 
# with the head node, ahead, and prev with NULL. Keep on iterating the linked list until 
# ‘curr’ reaches NULL. Store the next node of the current node in ‘ahead’ before changing 
# the next of the current node and point the next of the current node to ‘prev’ 
# (pointer to the node just before the current node). This is the actual reversing of the 
# links in the linked list. Point ‘prev’ node to ‘curr’ node and ‘curr’ node to ‘ahead’ node. 
# At the end return the head of the reversed linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def build_linked_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    curr = head

    for v in values[1:]:
        curr.next = ListNode(v)
        curr = curr.next

    return head
def print_linked_list(head):
    curr = head
    result = []

    while curr:
        result.append(str(curr.val))
        curr = curr.next

    print(" → ".join(result))

def reverseList(head):
    prev = None
    curr = head

    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    return prev


values = [1, 2, 3, 4, 5]
head = build_linked_list(values)

print_linked_list(head)

reversed_head = reverseList(head)
print_linked_list(reversed_head)