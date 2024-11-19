class Node:
    def __init__(self, value, next=None):
        self.val = value
        self.next = next
    def __repr__(self):
        return f"Node(val={self.val}, next={repr(self.next)})"
    
def list_to_linked_list(input_list):
    if not input_list:
        return None  # Return None if the list is empty

    head = Node(input_list[0])  # Create the head node
    current = head  # Initialize current node

    for value in input_list[1:]:
        current.next = Node(value)  # Create a new node and link it
        current = current.next  # Move to the new node

    return head  # Return the head of the linked list

def print_linked_list(head):
    current = head
    visited = set()
    
    while current is not None:
        if current in visited:  # Checking the actual node object, not its value
            print(f"{current.val} -> Cycle detected!")
            return
        print(current.val, end=" -> ")
        visited.add(current)  # Add the node itself (not the value) to the set
        current = current.next
    
    print("None")
