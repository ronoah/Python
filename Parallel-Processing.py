import concurrent.futures
from numpy import random
import time
import Plots

import Grid
import Resident
from Functions import infection_func, recovery_func, travel_func, red_zone_func
import Zone


NO_POLICY = 1
STAY_AT_HOME_POLICY = 2
SELF_QUARANTINE_POLICY = 3
RED_ZONES_POLICY = 4

POPULATION_NUM = 100000  # 300000
GRID_REC_SIZE = 92       # 160
ZONE_REC_SIZE = 23       # 40
RECOVERY_TIME_STEPS = 168  # 2688
RUNNING_TIME_STEPS = 1001  # 16000

RED_ZONE_CONDITION = 8     # 20


def do_zone_simulation(infected_res_id):
    print(f'Running Virus Spread Simulation for RED_ZONES_POLICY ...')

    sick_list = []

    # Step 1: create our data structures with even distribution
    grid = Grid.Grid(GRID_REC_SIZE)
    population_list = []
    tmp_r_id = 1
    while POPULATION_NUM + 1 > tmp_r_id:
        for y in range(1, GRID_REC_SIZE + 1):
            if tmp_r_id >= POPULATION_NUM:
                break
            for x in range(1, GRID_REC_SIZE + 1):
                res = Resident.Resident(tmp_r_id, x, y)
                population_list.append(res)

                cell = grid.get_cell(x, y)
                cell.set_resident(tmp_r_id)

                tmp_r_id += 1
                if tmp_r_id >= POPULATION_NUM + 1:
                    break
    # Step 2: creating list of all possible zones
    zones = []
    for y in range(1, GRID_REC_SIZE + 1):
        if y > GRID_REC_SIZE - ZONE_REC_SIZE:
            break
        for x in range(1, GRID_REC_SIZE + 1):
            if x <= GRID_REC_SIZE - ZONE_REC_SIZE:
                zone = Zone.Zone(x, y, ZONE_REC_SIZE, GRID_REC_SIZE)
                zones.append(zone)

    # Step 3: infecting resident and updating its cell
    print(f"Infecting resident id: {infected_res_id}")
    resident = population_list[infected_res_id - 1]
    resident.update_health_status(1)
    grid.get_cell(resident.cell_x, resident.cell_y).set_infected_resident(infected_res_id)

    total_infected_counter = 1
    total_recovered_counter = 0

    # Step 4: run the simulation
    for t in range(1, RUNNING_TIME_STEPS):
        new_infected = infection_func(population_list, grid)
        new_recovered = recovery_func(population_list, grid, RECOVERY_TIME_STEPS)
        red_zone_func(population_list, zones, grid, RED_ZONE_CONDITION)
        travel_func(population_list, grid, RED_ZONES_POLICY)

        total_infected_counter += new_infected
        total_recovered_counter += new_recovered
        current_sick_counter = total_infected_counter - total_recovered_counter

        sick_list.append(current_sick_counter)

        print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tt={:<3d} total sick={:<6d}'.format(t, current_sick_counter))

    return sick_list


def do_simulation(policy, infected_res_id):
    print(f'Running Virus Spread Simulation for policy {policy} ...')

    sick_list = []

    # Step 1: create our data structures with even distribution
    grid = Grid.Grid(GRID_REC_SIZE)
    population_list = []
    tmp_r_id = 1
    while POPULATION_NUM + 1 > tmp_r_id:
        for y in range(1, GRID_REC_SIZE + 1):
            if tmp_r_id >= POPULATION_NUM:
                break
            for x in range(1, GRID_REC_SIZE + 1):
                res = Resident.Resident(tmp_r_id, x, y)
                population_list.append(res)

                cell = grid.get_cell(x, y)
                cell.set_resident(tmp_r_id)

                tmp_r_id += 1
                if tmp_r_id >= POPULATION_NUM + 1:
                    break

    # Step 2: infecting resident and updating its cell
    print(f"Infecting resident id: {infected_res_id}")
    resident = population_list[infected_res_id - 1]
    resident.update_health_status(1)
    grid.get_cell(resident.cell_x, resident.cell_y).set_infected_resident(infected_res_id)

    total_infected_counter = 1
    total_recovered_counter = 0

    # Step 3: run the simulation
    for t in range(1, RUNNING_TIME_STEPS):
        new_infected = infection_func(population_list, grid)
        new_recovered = recovery_func(population_list, grid, RECOVERY_TIME_STEPS)
        travel_func(population_list, grid, policy)

        total_infected_counter += new_infected
        total_recovered_counter += new_recovered
        current_sick_counter = total_infected_counter - total_recovered_counter

        sick_list.append(current_sick_counter)

        if policy == 1:
            print('t={:<3d} total sick={:<6d}'.format(t, current_sick_counter))
        elif policy == 2:
            print('\t\t\t\t\t\t\t\t\tt={:<3d} total sick={:<6d}'.format(t, current_sick_counter))
        else:
            print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tt={:<3d} total sick={:<6d}'.format(t, current_sick_counter))

    return sick_list


if __name__ == '__main__':
    start = time.perf_counter()

    # choose randomly a resident ID to be infected
    r_id = random.randint(1, POPULATION_NUM + 1)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        p1 = executor.submit(do_simulation, 1, r_id)
        p2 = executor.submit(do_simulation, 2, r_id)
        p3 = executor.submit(do_simulation, 3, r_id)
        p4 = executor.submit(do_zone_simulation, r_id)

        # print(f'No Policy sick numbers {p1.result()}')
        # print(f'Stay At Home Policy sick numbers {p2.result()}')
        # print(f'Self Quarantine Policy sick numbers {p3.result()}')
        # print(p4.result())

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')

    # Create a graph
    Plots.plot_sick_func(p1.result(), p2.result(), p3.result(), p4.result(), RUNNING_TIME_STEPS)
