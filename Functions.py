from typing import List
from numpy import random
from sympy import exp
import Grid
import Resident
import Zone


def calc_q_based_on_policy_type(policy_type, sickness_status):
    if policy_type == 1:
        return 0.5
    elif policy_type == 2:
        return 0.9
    elif policy_type == 3 and (sickness_status == 0 or sickness_status == 2):
        return 0.5
    elif policy_type == 3 and sickness_status == 1:
        return 0.9


def travel_func(population_list: List[Resident.Resident], grid: Grid, policy_type):
    health_movement_counter = 0
    sick_movement_counter = 0
    r_and = random.rand()

    for res in population_list:
        if policy_type == 4:
            q_prob  = res.q_zone
        else:
            q_prob = calc_q_based_on_policy_type(policy_type, res.sickness_status)
        movement_prob = (1 - q_prob)  # probability to move in general

        movement_happened = False
        pre_movement_cell_x = res.cell_x
        pre_movement_cell_y = res.cell_y
        cell_type = grid.get_cell(res.cell_x, res.cell_y).type

        # the cell is in the middle, i.e. type 'A'
        if cell_type == 1:
            #t_start = time.perf_counter_ns()
            if r_and <= movement_prob:
                movement_happened = True
                movement_direction = random.randint(0,8)
                if movement_direction == 0:
                    res.cell_x -= 1
                    res.cell_y -= 1
                if movement_direction == 1:
                    res.cell_y -= 1
                if movement_direction == 2:
                    res.cell_x += 1
                    res.cell_y -= 1
                if movement_direction == 3:
                    res.cell_x -= 1
                if movement_direction == 4:
                    res.cell_x += 1
                if movement_direction == 5:
                    res.cell_x -= 1
                    res.cell_y += 1
                if movement_direction == 6:
                    res.cell_y += 1
                if movement_direction == 7:
                    res.cell_x += 1
                    res.cell_y += 1

            #t_end = time.perf_counter_ns()
            #print(f'Travel Cell Type 1 finished in {t_end - t_start} nano seconds')

        # the cell is wall adjacent, 'B'
        if 21 <= cell_type <= 24:
            if r_and <= movement_prob:
                movement_happened = True
                movement_direction = random.randint(0, 5)
                if cell_type == 21:
                    if movement_direction == 0:
                        res.cell_x -= 1
                    if movement_direction == 1:
                        res.cell_x += 1
                    if movement_direction == 2:
                        res.cell_x -= 1
                        res.cell_y += 1
                    if movement_direction == 3:
                        res.cell_y += 1
                    if movement_direction == 4:
                        res.cell_x += 1
                        res.cell_y += 1

                if cell_type == 22:
                    if movement_direction == 0:
                        res.cell_y -= 1
                    if movement_direction == 1:
                        res.cell_y += 1
                    if movement_direction == 2:
                        res.cell_x += 1
                        res.cell_y -= 1
                    if movement_direction == 3:
                        res.cell_x += 1
                    if movement_direction == 4:
                        res.cell_x += 1
                        res.cell_y += 1

                if cell_type == 23:
                    if movement_direction == 0:
                        res.cell_x -= 1
                    if movement_direction == 1:
                        res.cell_x += 1
                    if movement_direction == 2:
                        res.cell_x -= 1
                        res.cell_y -= 1
                    if movement_direction == 3:
                        res.cell_y -= 1
                    if movement_direction == 4:
                        res.cell_x += 1
                        res.cell_y -= 1

                if cell_type == 24:
                    if movement_direction == 0:
                        res.cell_y -= 1
                    if movement_direction == 1:
                        res.cell_y += 1
                    if movement_direction == 2:
                        res.cell_x -= 1
                        res.cell_y -= 1
                    if movement_direction == 3:
                        res.cell_x -= 1
                    if movement_direction == 4:
                        res.cell_x -= 1
                        res.cell_y += 1

        # the cell is in corner, 'C', there are 4 corners
        if 31 <= cell_type <= 34:
            if r_and <= movement_prob:
                movement_happened = True
                movement_direction = random.randint(0, 3)

                if cell_type == 31:
                    if movement_direction == 0:
                        res.cell_x += 1
                    if movement_direction == 1:
                        res.cell_y += 1
                    if movement_direction == 2:
                        res.cell_x += 1
                        res.cell_y += 1

                if cell_type == 32:
                    if movement_direction == 0:
                        res.cell_y -= 1
                    if movement_direction == 1:
                        res.cell_x += 1
                    if movement_direction == 2:
                        res.cell_x += 1
                        res.cell_y -= 1

                if cell_type == 33:
                    if movement_direction == 0:
                        res.cell_y -= 1
                    if movement_direction == 1:
                        res.cell_x -= 1
                    if movement_direction == 2:
                        res.cell_x -= 1
                        res.cell_y -= 1

                if cell_type == 34:
                    if movement_direction == 0:
                        res.cell_x -= 1
                    if movement_direction == 1:
                        res.cell_y += 1
                    if movement_direction == 2:
                        res.cell_x -= 1
                        res.cell_y += 1

        if movement_happened:
            # update cell location for both old and new cells
            grid.get_cell(pre_movement_cell_x, pre_movement_cell_y).remove_resident(res.id)
            grid.get_cell(res.cell_x, res.cell_y).set_resident(res.id)
            health_movement_counter += 1

            # set to default
            res.update_q_zone(0.5)

            if res.sickness_status == 0:
                res.consecutive_timesteps = 1

            if res.sickness_status == 1:
                grid.get_cell(res.cell_x, res.cell_y).set_infected_resident(res.id)
                grid.get_cell(pre_movement_cell_x, pre_movement_cell_y).remove_infected_resident(res.id)
                sick_movement_counter += 1


    #print(f"travel_func: health residents moved: {health_movement_counter}, sick residents moved: {sick_movement_counter}")


def calc_infection_probability(timesteps):
    return 1 - exp(-0.25 * timesteps)


# loop over all population, find all residents which are health (sickness == 0)
# and their cell is infected
def infection_func(population_list: List[Resident.Resident], grid: Grid):
    infected_counter = 0
    for resident in population_list:
        if resident.sickness_status == 0:
            cell = grid.get_cell(resident.cell_x, resident.cell_y)
            # todo : use method instead of len
            if len(cell.infected_residents_ids) > 0:
                # check probability that this resident will become sick
                prob = calc_infection_probability(resident.consecutive_timesteps)
                if random.random() <= prob:
                    resident.update_health_status(1)
                    cell.set_infected_resident(resident.id)
                    resident.consecutive_timesteps = 1
                    infected_counter += 1
                else:
                    resident.consecutive_timesteps += 1

    return infected_counter


def recovery_func(population_list: List[Resident.Resident], grid: Grid, recovery_time_steps):
    recover_counter = 0
    for resident in population_list:
        if resident.sickness_status == 1:
            if resident.consecutive_timesteps < recovery_time_steps:
                resident.consecutive_timesteps += 1
            else:
                cell = grid.get_cell(resident.cell_x, resident.cell_y)
                resident.update_health_status(2)
                cell.remove_infected_resident(resident.id)
                recover_counter += 1
    return recover_counter


def red_zone_func(population_list: List[Resident.Resident], zones: List[Zone.Zone], grid: Grid, red_zone_condition):
    for zone in zones:
        res_infected_in_zone = 0
        res_in_zone = []
        for cell_index in zone.cell_indexes:
            cell = grid.grid[cell_index - 1]
            res_infected_in_zone += len(cell.infected_residents_ids)

            if len(cell.infected_residents_ids) > 0:
                for r1 in cell.infected_residents_ids:
                    res_in_zone.append(r1)
            if len(cell.residents_ids) > 0:
                for r2 in cell.residents_ids:
                    res_in_zone.append(r2)

        if res_infected_in_zone > red_zone_condition:
            for res_id in res_in_zone:
                population_list[res_id - 1].update_q_zone(0.9)
