import time

class Soldoku:

    full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, field_str: str):
        self.grid = [[self.full_set.copy() for _ in range(9)] for _ in range(9)]
        rows = field_str.split(';')
        assert len(rows) == 9
        for r_idx, row in enumerate(rows):
            cells = row.split(',')
            assert len(cells) == 9
            for c_idx, cell in enumerate(cells):
                if cell.isdigit():
                    self.grid[r_idx][c_idx] = {int(cell)}

    def display(self):
        for row in self.grid:
            print(" | ".join("{" + ",".join(map(str, sorted(cell))) + "}" for cell in row))

    def reduce_all(self):
        for row_idx in range(9):
            for col_idx in range(9):
                self.reduce(row_idx, col_idx)

    def reduce(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9

        if len(self.grid[row_idx][col_idx]) == 1:
            return # nothing to reduce

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

    def get_total_number_of_set_values(self):
        """As lower this number, as more solved. Lowest value is 81."""
        cnt = 0
        for row in self.grid:
            for cell in row:
                cnt += len(cell)

        return cnt

# Example usage:
# sudoku = Soldoku("9,8,-,4,-,-,-,-,1;-,7,-,8,-,3,-,-,6;-,-,1,-,-,9,-,5,-;-,4,-,-,2,-,5,-,-;-,5,-,3,-,8,-,4,-;1,-,6,-,7,-,-,9,-;-,-,4,5,-,-,1,-,-;3,-,-,6,-,2,-,8,-;8,-,-,-,-,1,-,7,4")
# sudoku.display()
