import time
import copy
from typing import List

class Soldoku:

    full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, field_str=None, grid=None):
        if field_str is not None:
            self.grid = [[self.full_set.copy() for _ in range(9)] for _ in range(9)]
            rows = field_str.split(';')
            assert len(rows) == 9
            for r_idx, row in enumerate(rows):
                cells = row.split(',')
                assert len(cells) == 9
                for c_idx, cell in enumerate(cells):
                    if cell.isdigit():
                        self.grid[r_idx][c_idx] = {int(cell)}
        elif grid is not None:
            self.grid = copy.deepcopy(grid)
        else:
            self.grid = [[self.full_set.copy() for _ in range(9)] for _ in range(9)]

    def display(self):
        for row in self.grid:
            print(" | ".join("{" + ",".join(map(str, sorted(cell))) + "}" for cell in row))

    def solve(self) -> bool:
        accum_sizes, min_size, max_size = self.get_stats_of_set_values()
        while True:
            self.reduce_all()
            new_accum_sizes, min_size, max_size = self.get_stats_of_set_values()
            if new_accum_sizes == accum_sizes or min_size == 0:
                # no changes anymore or invalid solution
                break
            accum_sizes = new_accum_sizes

        if min_size == 1 and max_size == 1:
            return True # We found a valid solution
        elif min_size > 0 and max_size > 1:
            best_guesses = self.create_best_guesses()
            for guess in best_guesses:
                valid_guess = guess.solve()
                if valid_guess:
                    self.grid = guess.grid
                    return True

        return False

    def reduce_all(self):
        for row_idx in range(9):
            for col_idx in range(9):
                self.reduce(row_idx, col_idx)

    def reduce(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9

        #if len(self.grid[row_idx][col_idx]) == 1:
        #    return  # nothing to reduce

        for neighbour_sets in [self.get_neighbour_block_sets(row_idx, col_idx), self.get_neighbour_vertical_sets(row_idx, col_idx), self.get_neighbour_horizontal_sets(row_idx, col_idx)]:

            # if there is a fix value in neighbour set, then remove it from mine
            for s in neighbour_sets:
                if len(s) == 1:
                    self.grid[row_idx][col_idx] -= s

            # if I have a value in my set, which no neighbour set has, then I am this value
            for my_option in self.grid[row_idx][col_idx]:
                found_second_option = False
                for s in neighbour_sets:
                    if my_option in s:
                        found_second_option = True
                        break

                if not found_second_option:
                    self.grid[row_idx][col_idx] = {my_option}

    def get_neighbour_horizontal_sets(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9
        sets = []

        for cidx in range(9):
            if cidx != col_idx:
                sets.append(self.grid[row_idx][cidx])

        return sets

    def get_neighbour_vertical_sets(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9
        sets = []

        for ridx in range(9):
            if ridx != row_idx:
                sets.append(self.grid[ridx][col_idx])

        return sets

    def get_neighbour_block_sets(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9
        sets = []

        row_block_idx = row_idx // 3
        col_block_idx = col_idx // 3

        for ridx in range(3):
            row_idx_norm = row_block_idx * 3 + ridx
            for cidx in range(3):
                col_idx_norm = col_block_idx * 3 + cidx
                if (row_idx_norm != row_idx) or (col_idx_norm != col_idx):
                    sets.append(self.grid[row_idx_norm][col_idx_norm])

        return sets

    def create_best_guesses(self):
        # identify field with the least choices bigger than 1
        smallest_set_idx = 0, 0
        smallest_set_size_of_choices = 10
        for row_idx in range(9):
            for col_idx in range(9):
                set_size = len(self.grid[row_idx][col_idx])
                if set_size > 1 and set_size < smallest_set_size_of_choices:
                    smallest_set_size_of_choices = set_size
                    smallest_set_idx = row_idx, col_idx

        # create new grids by setting these choices
        best_guesses = []
        for option in self.grid[smallest_set_idx[0]][smallest_set_idx[1]]:
            new_grid = Soldoku(grid=self.grid)
            new_grid.grid[smallest_set_idx[0]][smallest_set_idx[1]] = {option}
            best_guesses.append(new_grid)

        return best_guesses


    def get_stats_of_set_values(self):
        """As lower this number, as more solved. Lowest value is 81. Further on, it gives the min set size and max set size"""
        cnt = 0
        min_set_size = 10
        max_set_size = 0
        for row in self.grid:
            for cell in row:
                set_size = len(cell)
                cnt += set_size
                min_set_size = min(min_set_size, set_size)
                max_set_size = max(max_set_size, set_size)

        return cnt, min_set_size, max_set_size
