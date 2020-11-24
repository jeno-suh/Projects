import unittest

from random_generator import RandomGenerator

class RandomGeneratorMethods(unittest.TestCase):
    def setUp(self):
        self.generator = RandomGenerator()
    
    def test_next(self):
        # Ensure that a sequence of seven tetriminoes produced by the 
        # generator has one of each kind of tetrimino
        tetrimino_lst = ["J", "L", "O", "I", "S", "Z", "T"]
        lst = []
        for i in range(7):
            lst.append(self.generator.next())
        self.assertEqual(lst.sort(), tetrimino_lst.sort())
    
if __name__ == '__main__':
    unittest.main()