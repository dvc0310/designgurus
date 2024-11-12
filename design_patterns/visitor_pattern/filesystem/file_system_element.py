from interface import FileSystemElement, Visitor

class File(FileSystemElement):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        
    def accept(self, visitor: Visitor):
        visitor.visitFile(self)

class Directory(FileSystemElement):
    def __init__(self, name):
        self.name = name
        self.children: list[FileSystemElement] = []  # Can contain Files or Directories

    def add(self, file: FileSystemElement):
        self.children.append(file)
    
    def accept(self, visitor: Visitor):
        visitor.visitDirectory(self)
        
class SizeCalculatorVisitor(Visitor):
    def __init__(self):
        self.total_size = 0

    def visitFile(self, file: File):
        print(f"Calculating size of file: {file.name} ({file.size} bytes)")
        self.total_size += file.size  
        
    def visitDirectory(self, directory: Directory):
        print(f"Entering directory: {directory.name}")
        for child in directory.children:
            child.accept(self)
        print(f"Exiting directory: {directory.name}")
        
class DisplayVisitor(Visitor):
    def __init__(self):
        self.indent_level = 0

    def visitFile(self, file: File):
        print('    ' * self.indent_level + f"- File: {file.name} ({file.size} bytes)")

    def visitDirectory(self, directory: Directory):
        print('    ' * self.indent_level + f"+ Directory: {directory.name}")
        self.indent_level += 1
        for child in directory.children:
            child.accept(self)
        self.indent_level -= 1
        
        