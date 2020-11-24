import unittest

from playfield import PlayField

class PlayFieldMethods(unittest.TestCase):
    def setUp(self):
        self.p = PlayField(10, 24)

    def test_init(self):
        with self.assertRaises(ValueError):
            self.p = PlayField(3, 24)
        with self.assertRaises(ValueError):
            self.p = PlayField(10, 5)
    
    def test_valid_square(self):
        self.assertTrue(self.p.valid_square(5,10))
        self.assertFalse(self.p.valid_square(10,24))
        self.assertFalse(self.p.valid_square(-1,10))
    
    def test_is_empty_square(self):
        self.assertTrue(self.p.is_empty_square(5,10))
        self.p._field[5][10] = "J"
        self.assertFalse(self.p.is_empty_square(5,10))
        with self.assertRaises(ValueError):
            self.p.is_empty_square(-1, 10)

    def test_get_square_kind(self):
        self.assertEqual(self.p.get_square_kind(5,10), None)
        self.p._field[5][10] = "J"
        self.assertEqual(self.p.get_square_kind(5,10), "J")
        with self.assertRaises(ValueError):
            self.p.get_square_kind(-1, 10)

    def test_row_is_full(self):
        self.assertFalse(self.p.row_is_full(10))
        for x in range(10):
            self.p._field[x][10] = "J"
        self.assertTrue(self.p.row_is_full(10))
        with self.assertRaises(ValueError):
            self.p.row_is_full(24)
    
    def test_clear_row(self):
        for x in range(10):
            self.p._field[x][23] = "J"
        for x in range(10):
            self.p._field[x][22] = "T"
        for x in range(5):
            self.p._field[x][21] = "O"
        self.p.clear_row(23)
        # Check if rows above have moved down
        for x in range(10):
            self.assertEqual(self.p.get_square_kind(x,23), "T")
        for x in range(5):
            self.assertEqual(self.p.get_square_kind(x,22), "O")
        for x in range(5, 10):
            self.assertTrue(self.p.is_empty_square(x,22))
        with self.assertRaises(ValueError):
            self.p.clear_row(24)
    
    def test_clear(self):
        for x in range(10):
            self.p._field[x][23] = "J"
        for x in range(10):
            self.p._field[x][22] = "T"
        for x in range(5):
            self.p._field[x][21] = "O"
        self.p.clear()
        for x in range(10):
            for y in range(24):
                self.assertTrue(self.p.is_empty_square(x, y))
    
    def test_lock_out(self):
        # Game not started
        self.assertFalse(self.p.lock_out())
        # Game lost to lock out
        for x in range(10):
            self.p._field[x][4] = "J"
        self.p.spawn("I")
        self.assertTrue(self.p.lock_out())
        self.p.clear()
        # Game not lost
        self.p.spawn("I")
        self.assertFalse(self.p.lock_out())
    
    def test_move_current(self):
        with self.assertRaises(AssertionError):
            self.p.move_current("down")
        self.p.spawn("J")
        self.p.move_current("down")
        self.assertEqual(self.p.get_square_kind(3,3), "J")
        self.assertEqual(self.p.get_square_kind(3,4), "J")
        self.assertEqual(self.p.get_square_kind(4,4), "J")
        self.assertEqual(self.p.get_square_kind(5,4), "J")
        self.p.clear()

        self.p.spawn("O")
        self.p.move_current("right")
        self.assertEqual(self.p.get_square_kind(5,2), "O")
        self.assertEqual(self.p.get_square_kind(5,3), "O")
        self.assertEqual(self.p.get_square_kind(6,2), "O")
        self.assertEqual(self.p.get_square_kind(6,3), "O")
        self.p.clear()

        self.p.spawn("T")
        self.p.move_current("left")
        self.assertEqual(self.p.get_square_kind(3,2), "T")
        self.assertEqual(self.p.get_square_kind(2,3), "T")
        self.assertEqual(self.p.get_square_kind(3,3), "T")
        self.assertEqual(self.p.get_square_kind(4,3), "T")
        self.p.clear()

        self.p.spawn("I")
        self.p.move_current("up")
        self.assertEqual(self.p.get_square_kind(3,2), "I")
        self.assertEqual(self.p.get_square_kind(4,2), "I")
        self.assertEqual(self.p.get_square_kind(5,2), "I")
        self.assertEqual(self.p.get_square_kind(6,2), "I")
        with self.assertRaises(ValueError):
            self.p.move_current("a")

    def test_rotate_current(self):
        # Note rotations based on SRS
        with self.assertRaises(AssertionError):
            self.p.rotate_current("left")
        self.p.spawn("S")
        self.p.rotate_current("left")
        self.assertEqual(self.p.get_square_kind(3,3), "S")
        self.assertEqual(self.p.get_square_kind(4,4), "S")
        self.assertEqual(self.p.get_square_kind(4,3), "S")
        self.assertEqual(self.p.get_square_kind(3,2), "S")
        self.p.clear()

        self.p.spawn("L")
        self.p.rotate_current("right")
        self.assertEqual(self.p.get_square_kind(4,3), "L")
        self.assertEqual(self.p.get_square_kind(4,2), "L")
        self.assertEqual(self.p.get_square_kind(4,4), "L")
        self.assertEqual(self.p.get_square_kind(5,4), "L")
        with self.assertRaises(ValueError):
            self.p.rotate_current("laft")

    def test_drop_current(self):
        with self.assertRaises(AssertionError):
            self.p.drop_current()
        self.p.spawn("Z")
        self.p.drop_current()
        self.assertEqual(self.p.get_square_kind(3,22), "Z")
        self.assertEqual(self.p.get_square_kind(4,22), "Z")
        self.assertEqual(self.p.get_square_kind(4,23), "Z")
        self.assertEqual(self.p.get_square_kind(5,23), "Z")

    def test_delete_current(self):
        with self.assertRaises(AssertionError):
            self.p.drop_current()
        self.p.spawn("I")
        self.p.delete_current()
        self.assertTrue(self.p.is_empty_square(3,3))
        self.assertTrue(self.p.is_empty_square(4,3))
        self.assertTrue(self.p.is_empty_square(5,3))
        self.assertTrue(self.p.is_empty_square(6,3))

    def test_spawn(self):
        self.p.spawn("J")
        self.assertEqual(self.p.get_square_kind(3,2), "J")
        self.assertEqual(self.p.get_square_kind(3,3), "J")
        self.assertEqual(self.p.get_square_kind(4,3), "J")
        self.assertEqual(self.p.get_square_kind(5,3), "J")
        self.p.clear()

        self.p.spawn("L")
        self.assertEqual(self.p.get_square_kind(5,2), "L")
        self.assertEqual(self.p.get_square_kind(3,3), "L")
        self.assertEqual(self.p.get_square_kind(4,3), "L")
        self.assertEqual(self.p.get_square_kind(5,3), "L")
        self.p.clear()

        self.p.spawn("O")
        self.assertEqual(self.p.get_square_kind(4,2), "O")
        self.assertEqual(self.p.get_square_kind(4,3), "O")
        self.assertEqual(self.p.get_square_kind(5,2), "O")
        self.assertEqual(self.p.get_square_kind(5,3), "O")
        self.p.clear()

        self.p.spawn("I")
        self.assertEqual(self.p.get_square_kind(3,3), "I")
        self.assertEqual(self.p.get_square_kind(4,3), "I")
        self.assertEqual(self.p.get_square_kind(5,3), "I")
        self.assertEqual(self.p.get_square_kind(6,3), "I")
        self.p.clear()

        self.p.spawn("S")
        self.assertEqual(self.p.get_square_kind(3,3), "S")
        self.assertEqual(self.p.get_square_kind(4,3), "S")
        self.assertEqual(self.p.get_square_kind(4,2), "S")
        self.assertEqual(self.p.get_square_kind(5,2), "S")
        self.p.clear()

        self.p.spawn("Z")
        self.assertEqual(self.p.get_square_kind(3,2), "Z")
        self.assertEqual(self.p.get_square_kind(4,2), "Z")
        self.assertEqual(self.p.get_square_kind(4,3), "Z")
        self.assertEqual(self.p.get_square_kind(5,3), "Z")
        self.p.clear()

        self.p.spawn("T")
        self.assertEqual(self.p.get_square_kind(4,2), "T")
        self.assertEqual(self.p.get_square_kind(3,3), "T")
        self.assertEqual(self.p.get_square_kind(4,3), "T")
        self.assertEqual(self.p.get_square_kind(5,3), "T")
        self.p.clear()
        with self.assertRaises(ValueError):
            self.p.spawn("A")

if __name__ == '__main__':
    unittest.main()