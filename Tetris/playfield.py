from __future__ import annotations
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from tetrimino import Tetrimino

from observer import Subject, Observer
from random_generator import RandomGenerator
from tetrimino import (TetriminoJ, TetriminoL, TetriminoO, TetriminoI,
                       TetriminoS, TetriminoZ, TetriminoT)

"""This module contains the PlayField class.

Classes:
- PlayField: Class for the field on which Tetris is played
"""

class PlayField(Observer, Subject):
    """This class represents the field on which Tetris is played.

    Note that this class acts as an observer to the tetriminoes that
    are played on it. It also acts as a subject to the AppFrame class
    which is the GUI that displays the entire Tetris app.

    Public Methods:
    - get_width() -> int
    - get_height() -> int
    - valid_square(x: int, y: int) -> bool
    - is_empty_square(x: int, y: int) -> bool
    - get_square_kind(x: int, y: int) -> Optional[str]
    - row_is_full(y: int) -> bool
    - clear_row(y: int) -> None
    - clear() -> None
    - lock_out() -> bool
    - move_current(dir_: str) -> bool
    - rotate_current(dir_: str_) -> bool
    - drop_current() -> None:
    - delete_current() -> str
    - spawn(kind: str) -> bool
    - update(subject: Tetrimino) -> None
    - add_observer(observer: Observer) -> None
    - notify_observers() -> None
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialise a playfield."""
        self._set_width(width)
        self._set_height(height)
        self._field = [[None for y in range(height)] for x in range(width)]
        """This private attribute reflects the state of the field.
        
        The top left square will be denoted by (0,0) and the bottom
        right square by (width-1,height-1). Note that the top four
        rows will be invisible to the player - the extra four rows only
        exist to spawn tetriminoes and to properly calculate a lock out
        loss. None will be used to denote that a square is empty; 
        otherwise, an appropriate string will denote the kind of block
        that occupies a square e.g. field[0][0] = "I" denotes that the
        top left square is occupied by a block from an "I" tetrimino.
        """
        self._current_tetrimino = None
        self._observers = []

    def get_width(self) -> int:
        """Getter method for self._width."""
        return self._width

    def _set_width(self, w: int) -> None:
        """Private setter method for self._width."""
        if w >= 4:
            self._width = w
        else:
            raise ValueError("Specified width is too small.")

    def get_height(self) -> int:
        """Getter method for self._height."""
        return self._height

    def _set_height(self, h: int) -> None:
        """Private setter method for self._height."""
        if h >= 8:
            self._height = h
        else:
            raise ValueError("Specified height is too short.")
    
    def _print(self) -> None:
        """Prints a representation of the playfield to the terminal.

        This function is useful for casual testing purposes."""
        print("+" + "---+"*self._width)
        for y in range(self._height):
            row_print = "|"
            for x in range(self._width):
                if self._field[x][y] == None:
                    row_print += "   |"
                else:
                    row_print += " " + self._field[x][y] + " |"
            print(row_print)
            print("+" + "---+"*self._width)
    
    def valid_square(self, x: int, y: int) -> bool:
        """Check if (x,y) denotes a valid square on the playfield."""
        return 0 <= x < self._width and 0 <= y < self._height
    
    def is_empty_square(self, x: int, y: int) -> bool:
        """Return whether a square is empty."""
        if not self.valid_square(x, y):
            raise ValueError("Invalid square specified.")
        return self._field[x][y] == None

    def get_square_kind(self, x: int, y: int) -> Optional[str]:
        """Return the kind of tetrimino block the specified square is
        occupied by; if it is empty, return None."""
        if not self.valid_square(x, y):
            raise ValueError("Invalid square specified.")
        return self._field[x][y]

    def _fill_square(self, x: int, y: int, kind: str) -> None:
        """Fill (x,y) with a block of the specified kind."""
        if not self.valid_square(x, y):
            raise ValueError("Invalid square specified.")
        if (kind == "J" or kind == "L" or kind == "O" or kind == "I"
            or kind == "S" or kind == "Z" or kind == "T"):
            self._field[x][y] = kind
        else:
            raise ValueError("Invalid kind of block specified.")

    def _empty_square(self, x: int, y: int) -> None:
        """Empty square (x,y)."""
        if self.valid_square(x, y):
            self._field[x][y] = None
        else:
            raise ValueError("Invalid square specified.")

    def _row_is_empty(self, y: int) -> bool:
        """Return whether a row is empty i.e. has no filled squares."""
        if not (0 <= y < self._height):
            raise ValueError("Invalid row specified.")
        for x in range(self._width):
            if self._field[x][y] != None:
                return False
        return True

    def row_is_full(self, y: int) -> bool:
        """Return whether a row is full i.e. has no empty squares."""
        if not (0 <= y < self._height):
            raise ValueError("Invalid row specified.")
        for x in range(self._width):
            if self._field[x][y] == None:
                return False
        return True

    def clear_row(self, y: int) -> None:
        """Clear a row i.e. make all its squares empty.
        
        Note that this has the side effect of moving all rows above
        down by one.
        """
        if not (0 <= y < self._height):
            raise ValueError("Invalid row specified.")
        for x in range(self._width):
            self._field[x][y] = None
        for y_ in range(y-1, 0, -1):
            self._move_row_down_one(y_)

    def _move_row_down_one(self, y_: int) -> None:
        """Move a row down by one.
        
        This is a helper function for clear_row. A precondition is that
        the row below be empty.
        """
        if not (0 <= y_ < self._height-1):
            raise ValueError("Invalid row specified.")
        if not self._row_is_empty(y_+1):
            raise ValueError("Row below is not empty.")
        for x in range(self._width):
            self._field[x][y_+1] = self._field[x][y_]
            self._field[x][y_] = None

    def clear(self) -> None:
        """Clear the field and current tetrimino."""
        for x in range(self._width):
            for y in range(self._height):
                self._empty_square(x, y)
        self._current_tetrimino = None
        self.notify_observers()

    def lock_out(self) -> bool:
        """Return whether or not a game of Tetris has been lost due to
        a lock out.
        """
        if self._current_tetrimino == None: # Game not started
            return False
        if self._current_tetrimino.move("down"): # Current tetrimino not set
            self._current_tetrimino.move("up")   # Restore state
            return False
        else: # Current tetrimino is set
            # Lock out loss if one of the top (invisible) four rows isn't empty
            lost = not (self._row_is_empty(0) and self._row_is_empty(1) \
                        and self._row_is_empty(2) and self._row_is_empty(3))
            return lost

    def move_current(self, dir_: str) -> bool:
        """Move the current tetrimino."""
        assert self._current_tetrimino != None, "No current tetrimino."
        moved = self._current_tetrimino.move(dir_)
        self.notify_observers()
        return moved

    def rotate_current(self, dir_: str) -> bool:
        """Rotate the current tetrimino."""
        assert self._current_tetrimino != None, "No current tetrimino."
        rotated = self._current_tetrimino.rotate(dir_)
        self.notify_observers()
        return rotated

    def drop_current(self) -> None:
        """Drop the current tetrimino."""
        assert self._current_tetrimino != None, "No current tetrimino."
        self._current_tetrimino.drop()
        self.notify_observers()

    def delete_current(self) -> str:
        """Delete the current tetrimino and return its kind."""
        assert self._current_tetrimino != None, "No current tetrimino."
        current = self._current_tetrimino
        self._current_tetrimino.delete()
        self.notify_observers()
        return current

    def spawn(self, kind: str) -> bool:
        """Spawn a new tetrimino of the specified kind in the 
        orientation and position outlined by the Tetris guideline.
        Return whether or not the spawn was successful."""
        if self._width % 2 == 0:
            # middle is left leaning with even width
            middle = self._width//2 - 1
        else:
            middle = self._width//2
        if kind == "J":
            self._current_tetrimino = TetriminoJ("north", (middle-1,2), self)
        elif kind == "L":
            self._current_tetrimino = TetriminoL("north", (middle-1,3), self)
        elif kind == "O":
            self._current_tetrimino = TetriminoO("north", (middle,2), self)
        elif kind == "I":
            self._current_tetrimino = TetriminoI("north", (middle-1,3), self)
        elif kind == "S":
            self._current_tetrimino = TetriminoS("north", (middle-1,3), self)
        elif kind == "Z":
            self._current_tetrimino = TetriminoZ("north", (middle-1,2), self)
        elif kind == "T":
            self._current_tetrimino = TetriminoT("north", (middle-1,3), self)
        else:
            raise ValueError("Invalid kind of tetrimino specified.")
        self.notify_observers()
        return self._current_tetrimino.spawned
            
    def update(self, subject: Tetrimino) -> None:
        for x, y in subject.get_prev_positions():
            self._empty_square(x, y)
        for x, y in subject.get_positions():
            self._fill_square(x, y, subject.kind)

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)