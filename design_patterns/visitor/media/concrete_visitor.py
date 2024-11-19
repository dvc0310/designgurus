from visitor import Visitor
from concrete_media import Book, DVD, Magazine, Library

class LibraryVisitor(Visitor):
    def __init__(self):
        self._total_cost = 0
        
    def visit_book(self, book: Book):
        print(f"Getting the cost of the Book: {book.get_title()} (${book.get_cost()})")
        self._total_cost += book.get_cost()
    
    def visit_DVD(self, DVD: DVD):
        print(f"Getting the cost of the DVD: {DVD.get_title()} (${DVD.get_cost()})")
        self._total_cost += DVD.get_cost()
    
    def visit_magazine(self, magazine: Magazine):
        print(f"Getting the cost of the Magazine: {magazine.get_title()} (${magazine.get_cost()})")
        self._total_cost += magazine.get_cost()
        
    def visit_library(self, library: Library):
        print(f"Entering Library: {library.name}")
        for child in library.get_library():
            child.accept(self)
        print(f"Exiting Library: {library.name}")
    
    def get_total_cost(self):
        return self._total_cost