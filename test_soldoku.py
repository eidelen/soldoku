import unittest
from soldoku import Soldoku

class Soldoku_Tests(unittest.TestCase):

    test_game = "9,8,4,3,-,7,-,-,6;-,-,-,-,-,-,-,-,3;-,6,-,5,-,-,-,7,-;-,9,8,-,-,-,3,-,4;-,-,-,-,4,-,-,-,-;4,-,3,-,-,-,7,9,-;-,7,-,-,-,4,-,1,-;2,-,-,-,-,-,-,-,-;6,-,-,7,-,1,8,4,5"
    test_game_false_row_less = "-,-,-,-,-,-,-,-,3;-,6,-,5,-,-,-,7,-;-,9,8,-,-,-,3,-,4;-,-,-,-,4,-,-,-,-;4,-,3,-,-,-,7,9,-;-,7,-,-,-,4,-,1,-;2,-,-,-,-,-,-,-,-;6,-,-,7,-,1,8,4,5"
    test_game_false_colval_less = "9,8,4,3,-,7,-,-,6;-,-,-,-,-,-,-,3;-,6,-,5,-,-,-,7,-;-,9,8,-,-,-,3,-,4;-,-,-,-,4,-,-,-,-;4,-,3,-,-,-,7,9,-;-,7,-,-,-,4,-,1,-;2,-,-,-,-,-,-,-,-;6,-,-,7,-,1,8,4,5"

    def test_ctor(self):
        dok = Soldoku(self.test_game)
        self.assertEqual(dok.grid[0][0], {9})
        self.assertEqual(dok.grid[2][1], {6})
        self.assertEqual(dok.grid[8][0], {6})
        self.assertEqual(dok.grid[1][0], dok.full_set)

    def test_ctor_assert(self):
        with self.assertRaises(AssertionError) as context:
            dok = Soldoku(self.test_game_false_row_less)
        with self.assertRaises(AssertionError) as context:
            dok = Soldoku(self.test_game_false_colval_less)

    def test_gethor(self):
        dok = Soldoku(self.test_game)
        sets = dok.get_neighbour_horizontal_sets(0, 1)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], {9})
        self.assertEqual(sets[1], {4})
        self.assertEqual(sets[2], {3})
        self.assertEqual(sets[3], dok.full_set)

    def test_getvert(self):
        dok = Soldoku(self.test_game)
        sets = dok.get_neighbour_vertical_sets(0, 1)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], dok.full_set)
        self.assertEqual(sets[1], {6})
        self.assertEqual(sets[2], {9})
        self.assertEqual(sets[3], dok.full_set)



