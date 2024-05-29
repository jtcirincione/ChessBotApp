class Piece:
    def __init__(self, name, color):
        self.color = color
        self.name = name
    pass

class Pawn(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
class Knight(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
class Bishop(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
class Rook(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
class King(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
class Queen(Piece):
    def __init__(self, name, color):
        super().__init__(name, color)
