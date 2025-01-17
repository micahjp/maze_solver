import random
from time import sleep
from cell import Cell
from point import Point


class Maze():
    def __init__(
            self,
            top_left_point,
            cell_size_x,
            cell_size_y,
            num_cols,
            num_rows,
            window=None,
            seed=None
    ):
        self._cells = None
        self.top_left_point = top_left_point
        self.cell_size_x = int(cell_size_x)
        self.cell_size_y = int(cell_size_y)
        self.num_cols = int(num_cols)
        self.num_rows = int(num_rows)
        self.window = window
        self._create_cells()
        self._break_entrance_and_exit()
        if seed:
            random.seed(seed)
        self._break_walls_r(self._cells[0][0])
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for row in range(self.num_rows):
            self._cells.append([])
            for column in range(self.num_cols):
                self._cells[row].append(Cell(self.window))
                if self.window:
                    self._draw_cell(self._cells[row][column], row, column)

    def _draw_cell(self, cell, row, column):
        cell_top_left = Point(column * self.cell_size_x,
                              row * self.cell_size_y) + self.top_left_point
        cell_bottom_right = Point(
            cell_top_left.x + self.cell_size_x,
            cell_top_left.y + self.cell_size_y
        )
        cell.draw(
            cell_top_left,
            cell_bottom_right
        )
        self._animate()

    def _animate(self):
        self.window.redraw()
        sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_rows - 1][self.num_cols -
                                       1].has_bottom_wall = False
        if self.window:
            self._draw_cell(self._cells[0][0], 0, 0)
            self._draw_cell(
                self._cells[self.num_rows - 1][self.num_cols - 1],
                self.num_rows - 1,
                self.num_cols - 1
            )

    def _break_walls_r(self, current_cell):
        current_cell.visited = True
        while True:
            neighbors = []
            for neighbor in self._get_cell_neighbors(current_cell):
                if not neighbor.visited:
                    neighbors.append(neighbor)
                else:
                    continue

            if not neighbors:
                return
            target_cell = neighbors[int(random.randrange(0, len(neighbors)))]

            if target_cell.top_left_point.x > current_cell.top_left_point.x:
                target_cell.has_left_wall = False
                current_cell.has_right_wall = False
            elif target_cell.top_left_point.x < current_cell.top_left_point.x:
                target_cell.has_right_wall = False
                current_cell.has_left_wall = False
            elif target_cell.top_left_point.y > current_cell.top_left_point.y:
                target_cell.has_top_wall = False
                current_cell.has_bottom_wall = False
            else:
                current_cell.has_top_wall = False
                target_cell.has_bottom_wall = False

            if self.window:
                current_cell.draw(current_cell.top_left_point,
                                  current_cell.bottom_right_point)
                target_cell.draw(target_cell.top_left_point,
                                 target_cell.bottom_right_point)
            self._break_walls_r(target_cell)

    def _get_cell_neighbors(self, cell):
        x_index = int(
            (cell.top_left_point.x - self.top_left_point.x) / self.cell_size_x)
        y_index = int(
            (cell.top_left_point.y - self.top_left_point.y) / self.cell_size_y)
        neighbors = []
        if y_index != 0:
            if y_index != self.num_rows - 1:
                neighbors.append(self._cells[y_index-1][x_index])
                neighbors.append(self._cells[y_index+1][x_index])
            else:
                neighbors.append(self._cells[y_index-1][x_index])
        else:
            neighbors.append(self._cells[y_index+1][x_index])

        if x_index != 0:
            if x_index != self.num_cols - 1:
                neighbors.append(self._cells[y_index][x_index-1])
                neighbors.append(self._cells[y_index][x_index+1])
            else:
                neighbors.append(self._cells[y_index][x_index-1])
        else:
            neighbors.append(self._cells[y_index][x_index+1])

        return neighbors

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False
