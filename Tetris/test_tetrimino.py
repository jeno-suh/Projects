import unittest

from playfield import PlayField
from tetrimino import (TetriminoJ, TetriminoL, TetriminoO, TetriminoI,
                       TetriminoS, TetriminoZ, TetriminoT)
class BaseTetriminoTests:
    class TetriminoMethods(unittest.TestCase):
        def test_move(self):
            positions = self.tetrimino.get_positions()
            up_positions = []
            left_positions = []
            for x, y in positions:
                up_positions.append((x,y-1))
                left_positions.append((x-1,y))
            move = self.tetrimino.move("up")
            self.assertTrue(move)
            self.assertEqual(self.tetrimino.get_positions(), up_positions)
            move = self.tetrimino.move("down")
            self.assertTrue(move)
            self.assertEqual(self.tetrimino.get_positions(), positions)
            move = self.tetrimino.move("left")
            self.assertTrue(move)
            self.assertEqual(self.tetrimino.get_positions(), left_positions)
            move = self.tetrimino.move("right")
            self.assertTrue(move)
            self.assertEqual(self.tetrimino.get_positions(), positions)
            # Check what happens when you can't move in the specified direction
            self.tetrimino.drop()
            drop_positions = self.tetrimino.get_positions()
            move = self.tetrimino.move("down")
            self.assertFalse(move)
            self.assertEqual(self.tetrimino.get_positions(), drop_positions)
            with self.assertRaises(ValueError):
                self.tetrimino.move("a")

        def _test_rotate_helper(self, lst, cant_rotate_case):
            """ A helper function for test_rotate.

            This helper function just makes the concise by preventing a
            lot of code repetition."""
            rotated = self.tetrimino.rotate("right")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[0])
            rotated = self.tetrimino.rotate("right")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[1])
            rotated = self.tetrimino.rotate("right")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[2])
            rotated = self.tetrimino.rotate("right")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[3])
            rotated = self.tetrimino.rotate("left")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[2])
            rotated = self.tetrimino.rotate("left")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[1])
            rotated = self.tetrimino.rotate("left")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[0])
            rotated = self.tetrimino.rotate("left")
            self.assertTrue(rotated)
            self.assertEqual(self.tetrimino.get_positions(), lst[3])
            with self.assertRaises(ValueError):
                self.tetrimino.rotate("up")
            if cant_rotate_case:
                # Dropping the tetrimino and rotating is sufficient to create a
                # case where rotating would move the tetrimino outside the field
                # for all tetriminoes except O (O can always rotate)
                self.tetrimino.drop()
                rotated = self.tetrimino.rotate("right")
                self.assertFalse(rotated)
        
        def test_drop(self):
            positions = self.tetrimino.get_positions()
            # Simulate a drop by moving the tetrimino down as much as you can
            while self.tetrimino.move("down"):
                pass
            drop_positions = self.tetrimino.get_positions()
            # Restore tetrimino to initial position
            self.tetrimino.delete()
            self.tetrimino._set_positions(positions[0])
            self.tetrimino.drop()
            self.assertEqual(self.tetrimino.get_positions(), drop_positions)
        
        def test_delete(self):
            positions = self.tetrimino.get_positions()
            self.tetrimino.delete()
            for x, y in positions:
                self.assertTrue(self.field.is_empty_square(x,y))

class TetriminoJMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoJ("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+1,y), (x+1,y+1), (x+1,y+2), (x+2, y)],
               [(x,y+1), (x+1,y+1), (x+2,y+1), (x+2,y+2)],
               [(x,y+2), (x+1,y), (x+1,y+1), (x+1,y+2)],
               [(x,y), (x,y+1), (x+1,y+1), (x+2,y+1)]]
        self._test_rotate_helper(lst, True)

class TetriminoLMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoL("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+1,y-1), (x+1,y), (x+1,y+1), (x+2, y+1)],
               [(x,y), (x,y+1), (x+1,y), (x+2,y)],
               [(x,y-1), (x+1,y-1), (x+1,y), (x+1,y+1)],
               [(x,y), (x+1,y), (x+2,y-1), (x+2,y)]]
        self._test_rotate_helper(lst, True)

class TetriminoOMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoO("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x,y), (x,y+1), (x+1,y), (x+1,y+1)]] * 4
        self._test_rotate_helper(lst, False)

class TetriminoIMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoI("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+2,y-1), (x+2,y), (x+2,y+1), (x+2, y+2)],
               [(x,y+1), (x+1,y+1), (x+2,y+1), (x+3,y+1)],
               [(x+1,y-1), (x+1,y), (x+1,y+1), (x+1,y+2)],
               [(x,y), (x+1,y), (x+2,y), (x+3,y)]]
        self._test_rotate_helper(lst, True)

class TetriminoSMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoS("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+1,y-1), (x+1,y), (x+2,y), (x+2, y+1)],
               [(x,y+1), (x+1,y), (x+1,y+1), (x+2,y)],
               [(x,y-1), (x,y), (x+1,y), (x+1, y+1)],
               [(x,y), (x+1,y-1), (x+1,y), (x+2,y-1)]]
        self._test_rotate_helper(lst, True)

class TetriminoZMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoZ("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+1,y+1), (x+1,y+2), (x+2,y), (x+2, y+1)],
               [(x,y+1), (x+1,y+1), (x+1,y+2), (x+2,y+2)],
               [(x,y+1), (x,y+2), (x+1,y), (x+1, y+1)],
               [(x,y), (x+1,y), (x+1,y+1), (x+2,y+1)]]
        self._test_rotate_helper(lst, True)

class TetriminoTMethods(BaseTetriminoTests.TetriminoMethods):
    def setUp(self):
        self.field = PlayField(10, 24)
        self.tetrimino = TetriminoT("north", (4,10), self.field)
    
    def test_rotate(self):
        x, y = self.tetrimino.get_positions()[0]
        lst = [[(x+1,y-1), (x+1,y), (x+1,y+1), (x+2, y)],
               [(x,y), (x+1,y), (x+1,y+1), (x+2,y)],
               [(x,y), (x+1,y-1), (x+1,y), (x+1,y+1)],
               [(x,y), (x+1,y-1), (x+1,y), (x+2,y)]]
        self._test_rotate_helper(lst, True)

if __name__ == '__main__':
    unittest.main()