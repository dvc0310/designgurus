class Node:
    def __init__(self, value, next=None):
        self.val = value
        self.next = next
    def __repr__(self):
        return f"Node(val={self.val}, next={repr(self.next)})"
    
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
