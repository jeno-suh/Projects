import unittest

from tictactoe import TicTacToe
from tictactoe_ai import RandomAI, WinningAI

class TestTicTacToeMethods(unittest.TestCase):
    def setUp(self):
        self.game = TicTacToe()

    def test_set_square(self):
        self.game.set_square(0, 0, "O")
        self.assertEqual(self.game.get_square(0, 0), "O")
        self.game.set_square(0, 0, "X")
        self.assertEqual(self.game.get_square(0, 0), "X")
        self.game.set_square(0, 0, None)
        self.assertEqual(self.game.get_square(0, 0), None)
        with self.assertRaises(ValueError):
            self.game.set_square(0, 0, "A")
        with self.assertRaises(TypeError):
            self.game.set_square(0, 0, 1)

    def test_make_move(self):
        # Valid move
        board = self.game.make_move(self.game._board, 0, 0, "O")
        self.assertEqual(board, [["O", None, None],
                                 [None, None, None],
                                 [None, None, None]])
        # Invalid move - square already occupied
        new_board = self.game.make_move(board, 0, 0, "X")
        self.assertEqual(new_board, [])
        # Invalid move - invalid square specified
        new_board2 = self.game.make_move(board, 3, 3, "X")
        self.assertEqual(new_board2, [])
        # Check board's state hasn't changed
        self.assertEqual(board, [["O", None, None],
                                 [None, None, None],
                                 [None, None, None]])

    def test_find_winner(self):
        # O wins diagonally
        board = [["O", "X", None],
                 [None, "O", None],
                 ["X", None, "O"]]
        winner = self.game.find_winner(board)
        self.assertEqual(winner, "O")
        # X wins vertically (board[x][y] occupies the (x, y) square)
        board = [["O", None, "O"],
                 [None, "O", None],
                 ["X", "X", "X"]]
        winner = self.game.find_winner(board)
        self.assertEqual(winner, "X")
        # O wins horizontally
        board = [["O", "X", "O"],
                 ["O", "X", "X"],
                 ["O", "O", "X"]]
        winner = self.game.find_winner(board)
        self.assertEqual(winner, "O")
        # Incomplete game
        board = [["O", "X", "O"],
                 [None, "X", "X"],
                 [None, "O", None]]
        winner = self.game.find_winner(board)
        self.assertEqual(winner, None)
        # Draw
        board = [["O", "O", "X"],
                 ["X", "X", "O"],
                 ["O", "X", "O"]]
        winner = self.game.find_winner(board)
        self.assertEqual(winner, None)
        # Two winners
        board = [["O", "X", None],
                 ["O", "X", None],
                 ["O", "X", None]]
        winner = self.game.find_winner(board)
        self.assertTrue(winner == "O" or winner == "X")

    def test_board_full(self):
        board = [["O", "X", "O"],
                 ["O", "X", "X"],
                 ["O", "O", "X"]]
        self.assertTrue(self.game.board_full(board))
        board = [["O", "X", "O"],
                 [None, "X", "X"],
                 [None, "O", None]]
        self.assertFalse(self.game.board_full(board))

    def test_load(self):
        self.game.load(RandomAI(self.game), "O")
        self.assertTrue(isinstance(self.game._O, RandomAI))
        self.game.load(WinningAI(self.game), "X")
        self.assertTrue(isinstance(self.game._X, WinningAI))
        with self.assertRaises(ValueError):
            self.game.load(RandomAI(self.game), "A")
        with self.assertRaises(TypeError):
            self.game.load(RandomAI(self.game), 1)

if __name__ == '__main__':
    unittest.main()