class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length
    
    def area(self):
        return self.length ** 2

shape = Shape()
print(f"Shape area: {shape.area()}")

square = Square(5)
print(f"Square area: {square.area()}")