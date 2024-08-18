import unittest
import time

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

    def test_getblock(self):
        dok = Soldoku(self.test_game)

        sets = dok.get_neighbour_block_sets(0, 0)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], {8})
        self.assertEqual(sets[1], {4})
        self.assertEqual(sets[2], dok.full_set)
        self.assertEqual(sets[3], dok.full_set)

        sets = dok.get_neighbour_block_sets(2, 0)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], {9})
        self.assertEqual(sets[1], {8})
        self.assertEqual(sets[2], {4})
        self.assertEqual(sets[3], dok.full_set)

        sets = dok.get_neighbour_block_sets(3, 7)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], {3})
        self.assertEqual(sets[1], {4})
        self.assertEqual(sets[2], dok.full_set)
        self.assertEqual(sets[3], dok.full_set)

        sets = dok.get_neighbour_block_sets(5, 7)
        self.assertEqual(len(sets), 8)
        self.assertEqual(sets[0], {3})
        self.assertEqual(sets[1], dok.full_set)
        self.assertEqual(sets[2], {4})
        self.assertEqual(sets[3], dok.full_set)


    def test_reduce(self):
        dok = Soldoku(self.test_game)
        dok.reduce(1, 0)

        self.assertEqual(dok.grid[1][0], {1, 5, 7})

    def test_num_set_vals(self):
        dok = Soldoku(self.test_game)

        should_be = 9 * 9 * 9 - (8 * 29)
        is_now = dok.get_total_number_of_set_values()

        self.assertEqual(should_be, is_now)

    def test_reduce_all(self):
        dok = Soldoku(self.test_game)
        print("Reducing:")
        num_set_vals_before = dok.get_total_number_of_set_values()
        for _ in range(6):
            dok.reduce_all()
            num_set_vals_after = dok.get_total_number_of_set_values()
            print("From ", num_set_vals_before, " to ", num_set_vals_after)
            num_set_vals_before = num_set_vals_after

        dok.display()

        #self.assertLess(num_set_vals_after, num_set_vals_before)

if __name__ == "__main__":
    test = Soldoku_Tests()
    test.test_reduce_all()



