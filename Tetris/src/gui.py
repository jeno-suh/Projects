from __future__ import annotations
from typing import List, Optional
from playfield import PlayField
import tkinter as tk
from tkinter import messagebox

from observer import Observer

"""This module contains the GUI classes used to display Tetris.

Classes:
- PlayFieldViewer
- SingleTetriminoViewer
- AppFrame
"""

class PlayFieldViewer(tk.Frame):
    """This class displays the PlayField.

    Recall that the first four rows of the playfield will be invisible
    to the player.
    
    Public methods:
    - update(field: PlayField) -> None
    """

    def __init__(self, parent, field) -> None:
        """Initialise display of the PlayField."""
        tk.Frame.__init__(self, parent)
        self._width = 25 * field.get_width()
        self._height = 25 * (field.get_height()-4)
        self._canvas = tk.Canvas(self, width=self._width, height=self._height)
        self._canvas.pack()
        self._rects = [[self._rect(x,y) for y in range(field.get_height()-4)] \
                       for x in range(field.get_width())]
        self._countdown_text = None
        self._pause_text_shown = False
        self._game_over_text_shown = False
        self.update(field)
    
    def _rect(self, x: int, y: int):
        """Create the (x,y) square at an appropriate positon on the
        screen and return it."""
        return self._canvas.create_rectangle(x*25, y*25, (x+1)*25, (y+1)*25)
        
    def _draw_squares(self) -> None:
        """Draw the squares into the display in a way that accurately
        portrays the specified PlayField."""
        for x in range(self._field.get_width()):
            for y in range(self._field.get_height()-4):
                self._canvas.itemconfig(self._rects[x][y], 
                                        fill=self._get_colour(x,y+4))

    def _get_colour(self, x: int, y: int) -> str:
        """Return the colour of (x,y) in self._field."""
        kind = self._field.get_square_kind(x,y)
        if kind == "J":
            return "blue"
        elif kind == "L":
            return "orange"
        elif kind == "O":
            return "yellow"
        elif kind == "I":
            return "cyan"
        elif kind == "S":
            return "green"
        elif kind == "Z":
            return "red"
        elif kind == "T":
            return "purple"
        elif kind == None:
            return "black"

    def countdown(self, n: int) -> None:
        """Display a countdown from n on the screen."""
        if n > 0:
            self._canvas.delete(self._countdown_text)
            self._countdown_text = self._canvas.create_text(self._width/2, 
                                                            self._height/2,
                                                            text=str(n),
                                                            fill="white")
            self.after(1000, self.countdown, n-1)
        elif n == 0:
            self._canvas.delete(self._countdown_text)
            self._countdown_text = self._canvas.create_text(self._width/2, 
                                                            self._height/2,
                                                            text="PLAY",
                                                            fill="white")
            self.after(1000, self._canvas.delete, self._countdown_text)
    
    def show_pause_text(self) -> None:
        """Display the text 'PAUSED' on the centre of the screen."""
        self._pause_text = self._canvas.create_text(self._width/2, 
                                                    self._height/2,
                                                    text="PAUSED",
                                                    fill="white")
        self._pause_text_shown = True

    def remove_pause_text(self) -> None:
        """Remove the 'PAUSED' text from the centre of the screen."""
        if self._pause_text_shown:
            self._canvas.delete(self._pause_text)
            self._pause_text_shown = False

    def show_game_over_text(self) -> None:
        """Display the text 'GAME OVER' on the centre of the screen."""
        self._game_over_text = self._canvas.create_text(self._width/2, 
                                                        self._height/2,
                                                        text="GAME OVER",
                                                        fill="white")
        self._game_over_text_shown = True

    def remove_game_over_text(self) -> None:
        """Remove the 'GAME OVER' text from the centre of the screen."""
        if self._game_over_text_shown:
            self._canvas.delete(self._game_over_text)
            self._game_over_text_shown = False

    def update(self, field: PlayField) -> None:
        """Update the display of the PlayField."""
        self._field = field
        self._draw_squares()

class SingleTetriminoViewer(PlayFieldViewer):
    """ This class displays a single tetrimino.
    
    Public Methods:
    - update(kind: Optional[str]) -> None
    """

    def __init__(self, parent, kind) -> None:
        """Initialise display of the tetrimino."""
        tk.Frame.__init__(self, parent)
        self._canvas = tk.Canvas(self, width=25*6, height=25*4)
        self._canvas.pack()
        self._field = PlayField(6, 8)
        self._rects = [[self._rect(x,y) for y in range(4)] \
                       for x in range(6)]
        self._kind = kind
        self.update(self._kind)

    def update(self, kind: Optional[str]) -> None:
        """Update display of the tetrimino."""
        self._field.clear()
        if kind != None:
            self._field.spawn(kind)
            self._field.drop_current()
            self._field.move_current("up")
        self._draw_squares()

class AppFrame(tk.Tk, Observer):
    """This class displays the entire application for Tetris.

    It acts as a facade, tying PlayFieldViewer together with various
    other UI elements e.g. a play button. It acts as an observer to
    PlayField.

    Public Methods:
    - get_key() -> Optional[str]
    - clear_key() -> None
    - game_over_dialog(lvl: int, score: int) -> None
    - update(field: PlayField) -> None
    - update_ui(lvl: int, score: int, playing: bool) -> None
    """

    def __init__(self, field: PlayField, app: Tetris) -> None:
        """Initialise the Tetris app display."""
        super().__init__()
        self.title("Tetris")
        self._app = app
        self._key_pressed = None
        self.bind_all("<Key>", self._handle_keypress)

        self._left = tk.Frame()
        self._hold_frame = tk.Frame(master=self._left, width=150)
        self._hold_lbl = tk.Label(master=self._hold_frame, text="Hold:")
        self._hold_lbl.pack(side=tk.LEFT)
        self._empty = tk.Label(master=self._hold_frame, text=" "*39)
        self._empty.pack(side=tk.RIGHT)
        self._hold_frame.pack(padx=10, pady=6)
        self._hold = SingleTetriminoViewer(self._left, None)
        self._hold.pack(padx=10)
        self._numbers = tk.Frame(master=self._left)
        self._lvl_lbl = tk.Label(master=self._numbers, text="Level:\n1")
        self._lvl_lbl.pack(padx=10)
        self._score_lbl = tk.Label(master=self._numbers, text="Score:\n0")
        self._score_lbl.pack(padx=10)
        self._numbers.pack(side=tk.BOTTOM, padx=10, pady=10)
        self._left.grid(row=0, column=0, sticky="nsew")

        self._viewer = PlayFieldViewer(self, field)
        self._viewer.grid(row=0, column=1, padx=10, pady=10)

        self._right = tk.Frame()
        self._next_frame = tk.Frame(master=self._right, width=150)
        self._next_lbl = tk.Label(master=self._next_frame, text="Next:")
        self._next_lbl.pack(side=tk.LEFT)
        self._empty = tk.Label(master=self._next_frame, text=" "*39)
        self._empty.pack(side=tk.RIGHT)
        self._next_frame.pack(padx=10, pady=6)
        self._next = SingleTetriminoViewer(self._right, None)
        self._next.pack(padx=10)
        self._buttons = tk.Frame(master=self._right)
        self._quit_btn = tk.Button(master=self._buttons, text="Quit",
                                   command=self.destroy)
        self._quit_btn.pack(padx=10)
        self._play_pause_btn = tk.Button(master=self._buttons, text="Play", 
                                         command=app.play_or_pause)
        self._play_pause_btn.pack(padx=10, pady=10)
        self._buttons.pack(side=tk.BOTTOM, padx=10, pady=5)
        self._right.grid(row=0, column=2, sticky="nsew")

        self.resizable(width=False, height=False)

    def _handle_keypress(self, event) -> None:
        """Handle keypresses by storing them in self._key_pressed.
        
        Note that only the latest keypress is stored.
        """
        self._key_pressed = event.keysym
    
    def get_key(self) -> Optional[str]:
        """Return the latest key pressed.
        
        Also sets self._key_pressed to None.
        """
        key_pressed = self._key_pressed
        self._key_pressed = None
        return key_pressed
    
    def clear_key(self) -> None:
        """Clear the latest key pressed."""
        self._key_pressed = None

    def countdown(self) -> None:
        """Display a countdown on the playfield to signal the start/
        continuation of a Tetris game."""
        self._viewer.countdown(3)
    
    def show_pause_text(self) -> None:
        """Display the text 'PAUSED' on the playfield."""
        self._viewer.show_pause_text()
    
    def remove_pause_text(self) -> None:
        """Remove the 'PAUSED' text from the playfield."""
        self._viewer.remove_pause_text()

    def show_game_over_text(self) -> None:
        """Display the text 'GAME OVER' on the playfield."""
        self._viewer.show_game_over_text()
    
    def remove_game_over_text(self) -> None:
        """Remove the text 'GAME OVER' from the playfield."""
        self._viewer.remove_game_over_text()

    def game_over_dialog(self, lvl: int, score: int) -> None:
        """Display a game over dialog box with the player's score and
        level."""
        messagebox.showinfo("Game Over", f"You got to level {lvl} with " +
                                         f"a score of {score}!")

    def update(self, field: PlayField) -> None:
        """Update the display of the field."""
        self._viewer.update(field)
    
    def update_ui(self, app: Tetris) -> None:
        """Update the display of other UI elements."""
        lvl = app.get_level()
        score = app.get_score()
        playing = app.get_playing()
        next_ = app.get_next()
        held = app.get_held()
        self._lvl_lbl.config(text=f"Level:\n{lvl}")
        self._score_lbl.config(text=f"Score:\n{score}")
        if playing:
            self._play_pause_btn.config(text="Pause")
        else:
            self._play_pause_btn.config(text="Play")
        self._next.update(next_)
        self._hold.update(held)