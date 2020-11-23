import tkinter as tk
from typing import List, Optional

from playfield import PlayField
from random_generator import RandomGenerator
from commands import (MoveCommand, RotateCommand, DropCommand, HoldCommand,
                      PlayPauseCommand)
from gui import AppFrame

"""This module contains the main application class and code to run the
program from the command line.

Classes:
- Tetris
"""

class Tetris:
    """This is the main application class.

    This class acts as the controller and contains the main gameplay
    loop. 
    
    Public Methods:
    - get_level() -> int
    - get_score() -> int
    - get_playing() -> bool
    - get_next() -> Optional[str]
    - get_held() -> Optional[str]
    - play_or_pause() -> None
    - drop() -> None
    - hold() -> None
    - activate() -> None
    """
    def __init__(self) -> None:
        """Initialise the Tetris application."""
        self._field = PlayField(10, 24)
        self._generator = RandomGenerator()
        self._keymap = {"Left": MoveCommand("left", self._field),
                        "Right": MoveCommand("right", self._field),
                        "Down": MoveCommand("down", self._field),
                        "space": DropCommand(self),
                        "Up": RotateCommand("right", self._field),
                        "x": RotateCommand("right", self._field),
                        "Control_L": RotateCommand("left", self._field),
                        "Control_R": RotateCommand("left", self._field),
                        "z": RotateCommand("left", self._field),
                        "Shift_L": HoldCommand(self),
                        "Shift_R": HoldCommand(self),
                        "c": HoldCommand(self),
                        "Escape": PlayPauseCommand(self)}
        self._valid_keys = self._keymap.keys()
        self._window = AppFrame(self._field, self)
        self._field.add_observer(self._window)
        self._fall_delay = 1000
        self._lock_delay = 500
        self._playing = False
        self._new_game = True
        self._counting_down = False
        self._level = 1
        self._progress_to_next_level = 0
        self._score = 0
        self._next_tetrimino = None
        self._held = None
        self._already_held = False

    def get_level(self) -> int:
        """Return the current level."""
        return self._level
    
    def get_score(self) -> int:
        """Return the current score."""
        return self._score

    def get_playing(self) -> bool:
        """Return whether or not a game of Tetris is being played."""
        return self._playing

    def get_next(self) -> Optional[str]:
        """Return the kind of tetrimino that will be played next."""
        return self._next_tetrimino

    def get_held(self) -> Optional[str]:
        """Return the kind of tetrimino currently being held."""
        return self._held

    def play_or_pause(self) -> None:
        """If a game of Tetris is playing, pause the game; otherwise,
        play the game."""
        if self._counting_down: # Can't activate while counting down
            return
        if self._playing:
            self._pause()
        else:
            self._play()

    def _play(self) -> None:
        """Start/Resume a game of Tetris."""
        self._window.clear_key()
        # Starting a new game
        if self._new_game:
            self._new_game = False
            self._field.clear()
            self._held = None
            self._field.spawn(self._generator.next())
            self._next_tetrimino = self._generator.next()
            self._window.remove_game_over_text()
        # Resuming a game
        else:
            self._window.remove_pause_text()
        self._counting_down = True
        self._window.countdown() # Takes 4 seconds
        self._window.after(4000, self._counting_down_false)
        self._window.after(4000, self._playing_true)
        self._window.after(4000, self._window.update_ui, self)
        self._window.after(4000, self._game_loop)
        self._window.after(4000, self._listen_to_keys)

    def _playing_true(self) -> None:
        """Set self._playing to be true."""
        self._playing = True

    def _counting_down_false(self) -> None:
        """Set self._counting_down to be false."""
        self._counting_down = False
    
    def _pause(self) -> None:
        """Pause a game of Tetris."""
        self._playing = False
        self._window.show_pause_text()
        self._window.update_ui(self)

    def drop(self) -> None:
        """Drop the current tetrimino."""
        self._field.drop_current()
        # Instantly lock
        rows_cleared = 0
        for y in range(self._field.get_height()):
            if self._field.row_is_full(y):
                self._field.clear_row(y)
                rows_cleared += 1
        self._update_scores_and_levels(rows_cleared)
        self._update_fall_delay()
        if self._game_over():
            self._playing = False
            self._new_game = True
            self._next_tetrimino = None
            self._window.update_ui(self)
            self._window.show_game_over_text()
            self._window.game_over_dialog(self._level, self._score)
        self._already_held = False # Can hold again

    def hold(self) -> None:
        """Hold the current tetrimino and spawn in the previously held
        tetrimino; if such a tetrimino does not exist, spawn a new 
        tetrimino."""
        if self._already_held: # Prevent infinitely spamming hold
            return             # without placing a tetrimino
        self._already_held = True
        prev_held = self._held
        self._held = self._field.delete_current().kind
        if prev_held == None:
            self._field.spawn(self._next_tetrimino)
            self._next_tetrimino = self._generator.next()
        else:
            self._field.spawn(prev_held)
        self._window.update_ui(self)

    def _game_loop(self) -> None:
        """The main gameplay loop for Tetris."""
        if self._playing:
            # Current tetrimino is set
            if not self._field.move_current("down"):
                self._already_held = False
                self._window.after(self._lock_delay, 
                                   self._set_current_tetrimino)
            # Current block has fallen one space
            else:
                self._window.after(self._fall_delay, self._game_loop)
    
    def _set_current_tetrimino(self) -> None:
        """Set the current tetrimino into place, clearing any filled
        rows, updating scores, levels and movement delay and check if
        the game is over."""
        if not self._field.move_current("down"):
            rows_cleared = 0
            for y in range(self._field.get_height()):
                if self._field.row_is_full(y):
                    self._field.clear_row(y)
                    rows_cleared += 1
            self._update_scores_and_levels(rows_cleared)
            self._update_fall_delay()
            if self._game_over():
                self._playing = False
                self._new_game = True
                self._next_tetrimino = None
                self._window.update_ui(self)
                self._window.game_over_dialog(self._level, self._score)
            self._window.after(0, self._game_loop)
        # User has moved block to where it can fall again
        else:
            self._window.after(self._fall_delay, self._game_loop)
    
    def _update_scores_and_levels(self, rows_cleared: int) -> None:
        """Update the score and level based on how many rows were
        cleared."""
        if rows_cleared == 1:
            self._progress_to_next_level += 1
            self._score += 100 * self._level
        elif rows_cleared == 2:
            self._progress_to_next_level += 3
            self._score += 300 * self._level
        elif rows_cleared == 3:
            self._progress_to_next_level += 5
            self._score += 500 * self._level
        elif rows_cleared == 4:
            self._progress_to_next_level += 8
            self._score += 800 * self._level
        if self._progress_to_next_level >= self._level * 5:
            self._progress_to_next_level -= self._level * 5
            self._level += 1
        self._window.update_ui(self)

    def _update_fall_delay(self) -> None:
        """Update the speed at which tetriminoes fall based on the
        current level."""
        self._fall_delay = (0.8 - (self._level-1) * 0.007) ** (self._level-1)
        self._fall_delay *= 1000
        self._fall_delay = int(self._fall_delay)

    def _game_over(self) -> bool:
        """Return whether the game is over.

        If the game is not over, this method has the side effect of
        spawning the next tetrimino."""
        over = (self._field.lock_out() 
                or not self._field.spawn(self._next_tetrimino))
        self._next_tetrimino = self._generator.next()
        self._window.update_ui(self)
        return over

    def _listen_to_keys(self) -> None:
        """Respond to user keyboard input."""
        if self._playing:
            key = self._window.get_key()
            if key in self._valid_keys:
                cmd = self._keymap[key]
                cmd.execute()
            self._window.after(10, self._listen_to_keys)
        else:
            key = self._window.get_key()
            if key == "Escape":         # If not playing only listen to the
                cmd = self._keymap[key] # escape key which pauses/plays the
                cmd.execute()           # game
            self._window.after(10, self._listen_to_keys)

    def activate(self) -> None:
        """Activate the application."""
        self._field.notify_observers()
        self._window.update_ui(self)
        self._window.mainloop()

if __name__ == "__main__":
    app = Tetris()
    app.activate()