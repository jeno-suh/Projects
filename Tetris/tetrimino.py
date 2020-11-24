from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
    from playfield import PlayField
from abc import ABC, abstractmethod

from observer import Subject, Observer

"""This module contains all tetrimino classes.

Classes:
- Tetrimino: An abstract base class for tetriminoes
- TetriminoJ: A concrete class for J tetriminoes
- TetriminoL: A concrete class for L tetriminoes
- TetriminoO: A concrete class for O tetriminoes
- TetriminoI: A concrete class for I tetriminoes
- TetriminoS: A concrete class for S tetriminoes
- TetriminoZ: A concrete class for Z tetriminoes
- TetriminoT: A concrete class for T tetriminoes
"""

class Tetrimino(Subject, ABC):
    """This is an abstract base class for tetriminoes.

    Note that this class (and its subclasses) act as subjects in the
    observer pattern, being observed by the field in which they are 
    played.
    
    Public Methods:
    - get_prev_positions() -> List[Tuple[int, int]]
    - get_positions() -> List[Tuple[int, int]]
    - move(dir_: str) -> bool
    - rotate(dir_: str) -> bool
    - drop() -> None
    - delete() -> None
    - add_observer(observer: Observer) -> None
    - notify_observers() -> None
    """

    @property
    @classmethod
    @abstractmethod
    def kind(cls):
        return NotImplementedError

    def __init__(self, ori: str, pos: Tuple[int, int], 
                 field: PlayField) -> None:
        """Initialise a tetrimino.
        
        Note that the pos argument refers to the square occupied by the
        leftmost and highest block of the tetrimino (with leftness
        having greater priorty than height). Further, an orientation
        of north refers to the orientation in which the tetrimino
        spawns; an orientation of east refers to the result of
        rotating the tetrimino 90 degrees clockwise from a northern
        orientation, etc.
        """
        self._prev_positions = []
        self._positions = []
        self._field = field
        self._observers = []
        self._set_orientation(ori)
        self.spawned = self._set_positions(pos)
        self.add_observer(field)
        self.notify_observers()

    def _set_orientation(self, ori: str) -> None:
        """Private setter method for self._orientation."""
        if ori == "north" or ori == "south" or ori == "east" or ori == "west":
            self._orientation = ori
        else:
            raise ValueError("Invalid tetrimino orientation specified.")

    def get_prev_positions(self) -> List[Tuple[int, int]]:
        """Getter method for self._prev_positions."""
        return self._prev_positions

    def get_positions(self) -> List[Tuple[int, int]]:
        """Getter method for self._positions, which is a list of all
        the squares on the playfield occupied by the tetrimino.
        
        Since this list will be sorted, its first element will denote
        the position of the leftmost and highest block of the tetrimino
        (with leftness having greater priority than height)."""
        return self._positions

    @abstractmethod
    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        """Private setter method for self._positions.
        
        The argument pos denotes the position of the leftmost and
        highest block of the tetrimino (with leftness having greater
        priority than height). In the case where the specified pos is
        invalid (e.g. would cause overlaps), this method will return
        false and not change any state."""
        pass
    
    def _set_positions_helper(self, pos: Tuple[int, int],
                              lst: List[List[Tuple[int, int]]]) -> bool:
        """A helper function for the _set_positions method.

        This helper function makes the code more concise by preventing
        a lot of code repetition in the _set_positions methods of the
        subclasses of the Tetrimino class.
        """
        assert (self._orientation == "north" or self._orientation == "south" or
                self._orientation == "east" or self._orientation == "west"),\
               "Invariant broken: self._orientation is not a valid orientation"
        if self._orientation == "north":
            new_positions = lst[0]
        elif self._orientation == "south":
            new_positions = lst[1]
        elif self._orientation == "east":
            new_positions = lst[2]
        elif self._orientation == "west":
            new_positions = lst[3]
        # Check that the new position occupies valid squares and won't occupy
        # non-empty squares (besides those currently occupied by itself)
        for x, y in new_positions:
            if (not (x, y) in self._positions
                and (not self._field.valid_square(x, y)
                or not self._field.is_empty_square(x, y))):
                return False
        self._prev_positions = self._positions
        self._positions = new_positions
        return True

    def move(self, dir_: str) -> bool:
        """Move the tetrimino one space in the specified direction.
        
        Returns True if movement succeeds; otherwise, no state is
        changed and returns False. Also returns True if the tetrimino
        has been deleted."""
        if self._positions == []:
            return True
        x, y = self._positions[0]
        if dir_ == "up":
            y -= 1
        elif dir_ == "down":
            y += 1
        elif dir_ == "left":
            x -= 1
        elif dir_ == "right":
            x += 1
        else:
            raise ValueError("Invalid direction specified.")
        if self._set_positions((x, y)):
            self.notify_observers()
            return True
        else:
            return False

    @abstractmethod
    def rotate(self, dir_: str) -> bool:
        """Rotate the tetrimino in the specified direction.
        
        In the case where the tetrimino cannot rotate in the specified
        direction, it returns False and no state is changed."""
        pass

    def _rotate_helper(self, dir_: str, lst: List[Tuple[int, int]]) -> bool:
        """A helper function for the rotate method.

        This helper function makes the code more concise by preventing
        a lot of code repetition in the rotate methods of the 
        subclasses of the Tetrimino class.
        """
        assert (self._orientation == "north" or self._orientation == "south" or
                self._orientation == "east" or self._orientation == "west"),\
               "Invariant broken: self._orientation is not a valid orientation"
        if dir_ != "left" and dir_ != "right":
            raise ValueError("Invalid rotation direction specified.")
        old_orientation = self._orientation
        if dir_ == "left":
            if self._orientation == "north":
                self._set_orientation("west")
                rotated = self._set_positions(lst[0])
            elif self._orientation == "south":
                self._set_orientation("east")
                rotated = self._set_positions(lst[1])
            elif self._orientation == "east":
                self._set_orientation("north")
                rotated = self._set_positions(lst[2])
            elif self._orientation == "west":
                self._set_orientation("south")
                rotated = self._set_positions(lst[3])
        elif dir_ == "right":
            if self._orientation == "north":
                self._set_orientation("east")
                rotated = self._set_positions(lst[4])
            elif self._orientation == "south":
                self._set_orientation("west")
                rotated = self._set_positions(lst[5])
            elif self._orientation == "east":
                self._set_orientation("south")
                rotated = self._set_positions(lst[6])
            elif self._orientation == "west":
                self._set_orientation("north")
                rotated = self._set_positions(lst[7])
        if rotated:
            self.notify_observers()
            return True
        else:
            self._set_orientation(old_orientation)
            return False

    def drop(self) -> None:
        """Drop the tetrimino."""
        prev_positions = self._positions
        x, y = self._positions[0]
        while self._set_positions((x, y)):
            y += 1
        self._prev_positions = prev_positions
        self.notify_observers()

    def delete(self) -> None:
        """Delete the tetrimino."""
        self._prev_positions = self._positions
        self._positions = []
        self.notify_observers()

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update(self)

class TetriminoJ(Tetrimino):
    """This is a class for the J tetrimino."""

    kind = "J"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x,y+1), (x+1,y+1), (x+2,y+1)], 
               [(x,y), (x+1,y), (x+2,y), (x+2,y+1)], 
               [(x,y), (x,y+1), (x,y+2), (x+1,y)], 
               [(x,y), (x+1,y-2), (x+1,y-1), (x+1,y)]]
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y+2), (x+1,y-1), (x-1,y), (x,y-1),
               (x+1,y), (x,y+1), (x-1,y+1), (x,y-2)]
        return self._rotate_helper(dir_, lst)

class TetriminoL(Tetrimino):
    """This is a class for the L tetrimino."""

    kind = "L"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x+1,y), (x+2,y-1), (x+2,y)],
               [(x,y), (x,y+1), (x+1,y), (x+2,y)],
               [(x,y), (x,y+1), (x,y+2), (x+1,y+2)],
               [(x,y), (x+1,y), (x+1,y+1), (x+1,y+2)]]
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y-1), (x+1,y-1), (x-1,y+1), (x,y+1),
               (x+1,y-1), (x,y-1), (x-1,y+1), (x,y+1)]
        return self._rotate_helper(dir_, lst)

class TetriminoO(Tetrimino):
    """This is a class for the O tetrimino."""

    kind = "O"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x,y+1), (x+1,y), (x+1,y+1)]] * 4
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y)] * 8
        return self._rotate_helper(dir_, lst)

class TetriminoI(Tetrimino):
    """This is a class for the I tetrimino."""

    kind = "I"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x+1,y), (x+2,y), (x+3,y)]] * 2 \
              + [[(x,y), (x,y+1), (x,y+2), (x,y+3)]] * 2
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x+1,y-1), (x+2,y-2), (x-2,y+1), (x-1,y+2),
               (x+2,y-1), (x+1,y-2), (x-2,y+2), (x-1,y+1)]
        return self._rotate_helper(dir_, lst)

class TetriminoS(Tetrimino):
    """This is a class for the S tetrimino."""

    kind = "S"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x+1,y-1), (x+1,y), (x+2,y-1)]] * 2 \
              + [[(x,y), (x,y+1), (x+1,y+1), (x+1,y+2)]] * 2
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y-1), (x+1,y-2), (x-1,y+1), (x,y+2),
               (x+1,y-1), (x,y-2), (x-1,y+2), (x,y+1)]
        return self._rotate_helper(dir_, lst)

class TetriminoZ(Tetrimino):
    """This is a class for the Z tetrimino."""

    kind = "Z"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x+1,y), (x+1,y+1), (x+2,y+1)]] * 2 \
              + [[(x,y), (x,y+1), (x+1,y-1), (x+1,y)]] * 2
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y+1), (x+1,y), (x-1,y-1), (x,y),
               (x+1,y+1), (x,y), (x-1,y), (x,y-1)]
        return self._rotate_helper(dir_, lst)

class TetriminoT(Tetrimino):
    """This is a class for the T tetrimino."""

    kind = "T"

    def _set_positions(self, pos: Tuple[int, int]) -> bool:
        x, y = pos
        lst = [[(x,y), (x+1,y-1), (x+1,y), (x+2,y)],
              [(x,y), (x+1,y), (x+1,y+1), (x+2,y)],
              [(x,y), (x,y+1), (x,y+2), (x+1,y+1)],
              [(x,y), (x+1,y-1), (x+1,y), (x+1,y+1)]]
        return self._set_positions_helper(pos, lst)
    
    def rotate(self, dir_: str) -> bool:
        x, y = self._positions[0]
        lst = [(x,y), (x+1,y-1), (x-1,y+1), (x,y),
               (x+1,y-1), (x,y), (x-1,y+1), (x,y)]
        return self._rotate_helper(dir_, lst)