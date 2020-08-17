from typing import List, Any


class Resident:
    def __init__(self, id, cell_x, cell_y, sickness_status=0):
        self.sickness_status = sickness_status  # 0 - healthy, 1 - sick, 2 - recovered
        self.id = id
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.consecutive_timesteps = 1
        self.q_zone = 0.5

    def increase_timesteps(self):
        self.consecutive_timesteps += 1

    def introduce_slf(self):
        if self.sickness_status == 0:
            print(f"ID:{self.id}, I'm healthy, cell_x:{self.cell_x} cell_y:{self.cell_y}")
        elif self.sickness_status == 1:
            print(f"ID:{self.id}, I'm sick, cell_x:{self.cell_x} cell_y:{self.cell_y}")
        else:
            print(f"ID:{self.id}, I Recovered, cell_x:{self.cell_x} cell_y:{self.cell_y}")

    def update_health_status(self, sickness_status):
        self.sickness_status = sickness_status

    def update_q_zone(self, q_zone):
        self.q_zone = q_zone


def calc_population_health_by_status(population_list: List[Resident], sickness_type: int):
    counter = 0
    for res in population_list:
        if res.sickness_status == sickness_type:
            counter += 1
    return counter
