class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left, self.right = None, None

def construct_binary_tree(values):
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    
    while i < len(values):
        current = queue.pop(0)
        
        if i < len(values) and values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    
    return root

def print_tree_structure(root, prefix="", is_left=True):
    """Prints the tree structure with the right node at the top and the left node at the bottom."""
    if root is not None:
        # Print the right child first with a right-aligned prefix
        print_tree_structure(root.right, prefix + ("    " if is_left else "    "), False)
        
        # Print the current node
        print(prefix + ("|-- " if is_left else "\\-- ") + str(root.val))
        
        # Print the left child with an aligned prefix
        print_tree_structure(root.left, prefix + ("    " if is_left else "    "), True)

