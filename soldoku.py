class Soldoku:

    full_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, field_str: str):
        self.grid = [[self.full_set for _ in range(9)] for _ in range(9)]
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

    def reduce(self, row_idx:int, col_idx:int):
        assert 0 <= row_idx < 9
        assert 0 <= col_idx < 9

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




# Example usage:
# sudoku = Soldoku("9,8,-,4,-,-,-,-,1;-,7,-,8,-,3,-,-,6;-,-,1,-,-,9,-,5,-;-,4,-,-,2,-,5,-,-;-,5,-,3,-,8,-,4,-;1,-,6,-,7,-,-,9,-;-,-,4,5,-,-,1,-,-;3,-,-,6,-,2,-,8,-;8,-,-,-,-,1,-,7,4")
# sudoku.display()
