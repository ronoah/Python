from typing import List


# Cell Type can be:
#     1 - middle cell, 'A'
#     21,22,23,34 - wall adjacent, 'B'
#     31,32,33,34 - corner cells, 'C'
def return_cell_type_func(cell_x, cell_y):
    cell_type = 1

    if cell_y == 1 and 2 <= cell_x <= Grid.GRID_RECTANGULAR_SIZE - 1:
        cell_type = 21
    if cell_x == 1 and 2 <= cell_y <= Grid.GRID_RECTANGULAR_SIZE - 1:
        cell_type = 22
    if cell_y == Grid.GRID_RECTANGULAR_SIZE and 2 <= cell_x <= Grid.GRID_RECTANGULAR_SIZE - 1:
        cell_type = 23
    if cell_x == Grid.GRID_RECTANGULAR_SIZE and 2 <= cell_y <= Grid.GRID_RECTANGULAR_SIZE - 1:
        cell_type = 24

    if cell_x == 1 and cell_y == 1:
        cell_type = 31
    if cell_x == 1 and cell_y == Grid.GRID_RECTANGULAR_SIZE:
        cell_type = 32
    if cell_x == Grid.GRID_RECTANGULAR_SIZE and cell_y == Grid.GRID_RECTANGULAR_SIZE:
        cell_type = 33
    if cell_x == Grid.GRID_RECTANGULAR_SIZE and cell_y == 1:
        cell_type = 34

    return cell_type


def return_cell_index_func(cell_x, cell_y):
    return (cell_y - 1) * Grid.GRID_RECTANGULAR_SIZE + cell_x


class Cell:
    def __init__(self, cell_x, cell_y):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.residents_ids = []
        self.infected_residents_ids = []
        self.type = return_cell_type_func(cell_x, cell_y)
        self.index = return_cell_index_func(self.cell_x, self.cell_y)

    def set_resident(self, resident_id: int):
        self.residents_ids.append(resident_id)

    def remove_resident(self, resident_id: int):
        self.residents_ids.remove(resident_id)

    def set_infected_resident(self, resident_id: int):
        self.infected_residents_ids.append(resident_id)

    def remove_infected_resident(self, resident_id: int):
        self.infected_residents_ids.remove(resident_id)

    def introduce_slf(self):
        print(f"Cell_{self.index} x:{self.cell_x} y:{self.cell_y} type:{self.type}")
        print(f"\tResidents: {self.residents_ids}, infected residents:{self.infected_residents_ids}")


class Grid:
    def __init__(self, rect_size):
        self.grid: List[Cell] = []

        Grid.GRID_RECTANGULAR_SIZE = rect_size
        for y in range(1, Grid.GRID_RECTANGULAR_SIZE + 1):
            for x in range(1, Grid.GRID_RECTANGULAR_SIZE + 1):
                cell = Cell(x, y)
                self.grid.append(cell)

    def get_cell(self, cell_x: int, cell_y: int):
        cell_idx = return_cell_index_func(cell_x, cell_y)
        return self.grid[cell_idx - 1]

    def introduce_slf(self):
        for i in self.grid:
            i.introduce_slf()
