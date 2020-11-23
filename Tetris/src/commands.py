from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from playfield import PlayField
    from tetris import Tetris
from abc import ABC, abstractmethod

"""This module contains the command classes for Tetris.

Classes:
- Command
- MoveCommand
- RotateCommand
- DropCommand
"""

class Command(ABC):
    """A simple interface for a command.

    Public Methods:
    - execute()
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

class MoveCommand(Command):
    """A command that moves the current block in the specified field in
    the specified direction.
    
    Public Methods:
    - execute()
    """

    def __init__(self, dir_: str, field: PlayField):
        if dir_ != "left" and dir_ != "right" and dir_ != "down":
            raise ValueError("Invalid movement direction specified.")
        self._dir = dir_
        self._field = field

    def execute(self) -> None:
        self._field.move_current(self._dir)

class RotateCommand(Command):
    """A command that rotates the current block in the specified field
    in the specified direction.

    Public Methods:
    - execute()
    """

    def __init__(self, dir_: str, field: PlayField):
        if dir_ != "left" and dir_ != "right":
            raise ValueError("Invalid movement direction specified.")
        self._dir = dir_
        self._field = field

    def execute(self) -> None:
        self._field.rotate_current(self._dir)

class DropCommand(Command):
    """A command that drops the current block in the specified field.

    Public Methods:
    - execute() -> None
    """

    def __init__(self, app: Tetris):
        self._app = app

    def execute(self) -> None:
        self._app.drop()

class HoldCommand(Command):
    """A command that holds the current block in the specified field.

    Public Methods:
    - execute()
    """

    def __init__(self, app: Tetris):
        self._app = app

    def execute(self) -> None:
        self._app.hold()

class PlayPauseCommand(Command):
    """A command that plays/pauses the Tetris game.

    Public Methods:
    - execute()
    """

    def __init__(self, app: Tetris):
        self._app = app
    
    def execute(self) -> None:
        self._app.play_or_pause()