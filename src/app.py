from enum import Enum
from typing import List


class Color(Enum):
    NONE = 0
    RED = 1
    BLUE = 2

    @property
    def opposite(self):
        if self is Color.NONE:
            return self
        elif self is Color.RED:
            return Color.BLUE
        else:
            return Color.RED


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Coordinate(new_x, new_y)

    @property
    def valid(self):
        return 0 <= self.x < 5 and 0 <= self.y < 5


class Delta:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self._opposite = None

    @property
    def opposite(self):
        if self._opposite is None:
            self._opposite = Delta(-self.x, -self.y)
            self._opposite._opposite = self
        return self._opposite


class Movement(Enum):
    TWO_FORWARD = (2, 0)
    KNIGHT_LEFT = (1, -2)
    FORWARD_LEFT = (1, -1)
    ONE_FORWARD = (1, 0)
    FORWARD_RIGHT = (1, 1)
    KNIGHT_RIGHT = (1, 2)
    TWO_LEFT = (0, -2)
    ONE_LEFT = (0, -1)
    ONE_RIGHT = (0, 1)
    TWO_RIGHT = (0, 2)
    BACK_LEFT = (-1, -1)
    ONE_BACK = (-1, 0)
    BACK_RIGHT = (-1, 1)

    def __init__(self, forward: int, right: int):
        self._delta = Delta(forward, right)

    def delta(self, color: Color) -> Delta:
        return self._delta if color is Color.RED else self._delta.opposite


class Card(Enum):
    BOAR = (Color.RED, [Movement.ONE_FORWARD, Movement.ONE_LEFT, Movement.ONE_RIGHT])
    COBRA = (Color.RED, [Movement.FORWARD_RIGHT, Movement.ONE_LEFT, Movement.BACK_RIGHT])
    CRAB = (Color.BLUE, [Movement.ONE_FORWARD, Movement.TWO_LEFT, Movement.TWO_RIGHT])
    CRANE = (Color.BLUE, [Movement.ONE_FORWARD, Movement.BACK_LEFT, Movement.BACK_RIGHT])
    DRAGON = (Color.RED, [Movement.KNIGHT_LEFT, Movement.KNIGHT_RIGHT, Movement.BACK_LEFT, Movement.BACK_RIGHT])
    EEL = (Color.BLUE, [Movement.FORWARD_LEFT, Movement.ONE_RIGHT, Movement.BACK_LEFT])
    ELEPHANT = (Color.RED, [Movement.FORWARD_LEFT, Movement.FORWARD_RIGHT, Movement.ONE_LEFT, Movement.ONE_RIGHT])
    FROG = (Color.RED, [Movement.FORWARD_LEFT, Movement.TWO_LEFT, Movement.BACK_RIGHT])
    GOOSE = (Color.BLUE, [Movement.FORWARD_LEFT, Movement.ONE_LEFT, Movement.ONE_RIGHT, Movement.BACK_RIGHT])
    HORSE = (Color.RED, [Movement.ONE_FORWARD, Movement.ONE_LEFT, Movement.ONE_BACK])
    MANTIS = (Color.RED, [Movement.FORWARD_LEFT, Movement.FORWARD_RIGHT, Movement.ONE_BACK])
    MONKEY = (Color.BLUE, [Movement.FORWARD_LEFT, Movement.FORWARD_RIGHT, Movement.BACK_LEFT, Movement.BACK_RIGHT])
    OX = (Color.BLUE, [Movement.ONE_FORWARD, Movement.ONE_RIGHT, Movement.ONE_BACK])
    RABBIT = (Color.BLUE, [Movement.FORWARD_RIGHT, Movement.TWO_RIGHT, Movement.BACK_LEFT])
    ROOSTER = (Color.RED, [Movement.FORWARD_RIGHT, Movement.ONE_LEFT, Movement.ONE_RIGHT, Movement.BACK_LEFT])
    TIGER = (Color.BLUE, [Movement.TWO_FORWARD, Movement.ONE_BACK])

    def __init__(self, color: Color, movements: List[Movement]):
        self.color = color
        self.movements = movements


class PieceType(Enum):
    NONE = 0
    STUDENT = 1
    MASTER = 2


class Piece(Enum):
    NONE = (Color.NONE, PieceType.NONE)
    RED_STUDENT = (Color.RED, PieceType.STUDENT)
    RED_MASTER = (Color.RED, PieceType.MASTER)
    BLUE_STUDENT = (Color.BLUE, PieceType.STUDENT)
    BLUE_MASTER = (Color.BLUE, PieceType.MASTER)

    def __init__(self, color: Color, piece_type: PieceType):
        self.color = color
        self.type = piece_type


class Move:
    def __init__(self, coordinate: Coordinate, card: Card, movement: Movement):
        self.coordinate = coordinate
        self.card = card
        self.movement = movement

    def destination(self, color: Color) -> Coordinate:
        return self.coordinate + self.movement.delta(color)

    def valid(self, color: Color) -> bool:
        return self.movement in self.card.movements and self.destination(color).valid


if __name__ == '__main__':
    possible_moves = []
    for x in range(5):
        for y in range(5):
            coordinate = Coordinate(x, y)
            for card in Card:
                for movement in card.movements:
                    move = Move(coordinate, card, movement)
                    if move.valid(Color.RED):
                        possible_moves.append(move)
    print(len(possible_moves))
    for move in possible_moves:
        print(f"  ({move.coordinate.x}, {move.coordinate.y}), {move.card}, {move.movement}")
