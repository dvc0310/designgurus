class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if not isinstance(other, Point):
            raise TypeError("The object being compared must be an instance of Point.")
        return self.distance_from_origin() > other.distance_from_origin()
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def distance_from_origin(self):
        return (self.x * self.x) + (self.y * self.y)

def convert_to_points(list_of_tuples):
    return [Point(x, y) for x, y in list_of_tuples]