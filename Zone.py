from Grid import return_cell_index_func


def return_cell_indexes_func(cell_x, cell_y, zone_rec_size, grid_rec_size):
    indexes = []
    for y in range(1, zone_rec_size + 1):
        for x in range(1, zone_rec_size + 1):
            idx = return_cell_index_func(x + cell_x - 1, y + cell_y - 1)
            indexes.append(idx)

    if len(indexes) < 529:
        print(f'number of cells={len(indexes)}, cell_x={cell_x}, cell_y={cell_y}')
    return indexes


class Zone:
    def __init__(self, cell_x, cell_y, zone_rec_size, grid_rec_size):
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.cell_indexes = []
        self.zone_rec_size = zone_rec_size
        self.cell_indexes = return_cell_indexes_func(cell_x, cell_y, zone_rec_size, grid_rec_size)

