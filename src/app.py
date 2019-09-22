from enum import Enum
from typing import List
import random


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

    def __eq__(self, other):
        return isinstance(other, Coordinate) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.y * 5 + self.x

    def __repr__(self):
        return f'({self.x}, {self.y})'


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
        self._delta = Delta(right, -forward)

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


def get_possible_moves() -> List[Move]:
    # There are 903 possible moves in Onitama.  Only a small number of them will be legal in any given position.
    possible_moves: List[Move] = []
    for x in range(5):
        for y in range(5):
            coordinate = Coordinate(x, y)
            for card in Card:
                for movement in card.movements:
                    move = Move(coordinate, card, movement)
                    if move.valid(Color.RED):
                        possible_moves.append(move)
    return possible_moves


ALL_MOVES = get_possible_moves()


class HandState:
    def __init__(self, cards: List[Card] = None, source=None):
        if source is not None:
            self.hands = {Color.RED: set(source.hands[Color.RED]), Color.BLUE: set(source.hands[Color.BLUE])}
            self.reserve = source.reserve
        else:
            self.hands = {Color.RED: set(), Color.BLUE: set()}
            if cards is None:
                candidates = [x for x in Card]
                random.shuffle(candidates)
                cards = candidates[0:5]
            self.hands[Color.RED].add(cards[0])
            self.hands[Color.RED].add(cards[1])
            self.hands[Color.BLUE].add(cards[2])
            self.hands[Color.BLUE].add(cards[3])
            self.reserve = cards[4]

    def play(self, color: Color, card: Card):
        if card not in self.hands[color]:
            raise Exception('Invalid play.')
        next_state = HandState(source=self)
        next_state.hands[color].remove(card)
        next_state.hands[color].add(next_state.reserve)
        next_state.reserve = card


class ZobristIndex:
    def __init__(self):
        r = random.Random(0xbadf00d)
        self.start = r.getrandbits(64)
        self.cards = {card: {color: r.getrandbits(64) for color in Color} for card in Card}
        self.board = {
            Coordinate(x, y): {
                piece: r.getrandbits(64) for piece in Piece
            }
            for x in range(5)
            for y in range(5)
        }


ZOBRIST = ZobristIndex()


class Board:
    def __init__(self, source=None):
        if source is not None:
            self.cells = {coordinate: piece for coordinate, piece in source.cells.items()}
            self.zobrist: int = source.zobrist
        else:
            self.cells = {}
            self.zobrist: int = ZOBRIST.start
            for y in range(5):
                for x in range(5):
                    coordinate = Coordinate(x, y)
                    if 0 < y < 4:
                        piece = Piece.NONE
                    elif x == 2:
                        piece = Piece.BLUE_MASTER if y == 0 else Piece.RED_MASTER
                    else:
                        piece = Piece.BLUE_STUDENT if y == 0 else Piece.RED_STUDENT
                    self.cells[coordinate] = piece
                    self.zobrist ^= ZOBRIST.board[coordinate][piece]

    def __getitem__(self, item: Coordinate):
        return self.cells[item]

    def __setitem__(self, key: Coordinate, value: Piece):
        old = self[key]
        if old == value:
            return
        self.zobrist ^= ZOBRIST.board[key][old]
        self.cells[key] = value
        self.zobrist ^= ZOBRIST.board[key][value]


if __name__ == '__main__':
    print(len(ALL_MOVES))
    board = Board()
    print(board.zobrist)
    for y in range(5):
        line = ''
        for x in range(5):
            coordinate = Coordinate(x, y)
            piece = board[coordinate]
            if piece is Piece.NONE:
                line += '_ '
            elif piece is Piece.BLUE_STUDENT:
                line += 'b '
            elif piece is Piece.BLUE_MASTER:
                line += 'B '
            elif piece is Piece.RED_STUDENT:
                line += 'r '
            else:
                line += 'R '
        print(line.rstrip())
