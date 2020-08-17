import time
import Resident
import Grid
import Plots
from numpy import random
from Functions import infection_func, recovery_func, travel_func
import simpy


random.seed()

POPULATION_NUM = 100000  # 300000
GRID_REC_SIZE = 92       # 160
NO_POLICY = 1
STAY_AT_HOME_Policy = 2
SELF_QUARANTINE_POLICY = 3
RED_ZONES_POLICY = 4
RECOVERY_TIME_STEPS = 168  # 2688
TIME_STEPS = 1001

no_policy_sick_list = []
stay_at_home_policy_sick_list = []
self_quarantine_policy_sick_list = []

##########################
# NO Policy Simulation
##########################
# Create the Haifa Grid, with empty residents
no_policy_grid = Grid.Grid(GRID_REC_SIZE)

# Create list of ALL residents with:
# healthy status, uniform (even) distribution within the cells
# Add resident to its Cell
no_policy_population_list = []
r_id: int = 1
while POPULATION_NUM+1 > r_id:
    for y in range(1, GRID_REC_SIZE + 1):
        if r_id >= POPULATION_NUM:
            break
        for x in range(1, GRID_REC_SIZE + 1):
            res = Resident.Resident(r_id, x, y)
            no_policy_population_list.append(res)

            cell = no_policy_grid.get_cell(x, y)
            cell.set_resident(r_id)

            r_id += 1
            if r_id >= POPULATION_NUM+1:
                break

# infect one random resident and update its cell
r_id = random.randint(1, POPULATION_NUM+1)
print(f"Infecting resident id: {r_id}")
resident = no_policy_population_list[r_id-1]
resident.update_health_status(1)
no_policy_grid.get_cell(resident.cell_x, resident.cell_y).set_infected_resident(r_id)
no_policy_grid.get_cell(resident.cell_x, resident.cell_y).introduce_slf()

total_infected_counter = 1
total_recovered_counter = 0
total_currentsick_counter = 0

for t in range(1, TIME_STEPS):
    t_start = time.perf_counter()

    new_infected = infection_func(no_policy_population_list, no_policy_grid)
    new_recovered = recovery_func(no_policy_population_list, no_policy_grid, RECOVERY_TIME_STEPS)
    #print('t={:<6d} Infected={:<6d} Recovered={:<6d} Totals: Sicks:{:<6d} Recovers:{:<6d}'.format(t,new_infected,new_recovered,total_infected_counter,total_recovered_counter))
    travel_func(no_policy_population_list, no_policy_grid, NO_POLICY)

    total_infected_counter += new_infected
    total_recovered_counter += new_recovered
    total_currentsick_counter = total_infected_counter - total_recovered_counter
    no_policy_sick_list.append(total_currentsick_counter)

    print('t={:<6d} totalsick={:<6d}'.format(t, total_currentsick_counter))
    t_end = time.perf_counter()
    #print(f'Finished in {t_end-t_start} seconds')

##########################
# stay at home Policy Simulation
##########################
# Create the Haifa Grid, with empty residents
stay_at_home_grid = Grid.Grid(GRID_REC_SIZE)

# Create list of ALL residents with:
# healthy status, uniform (even) distribution within the cells
# Add resident to its Cell
stay_at_home_population_list = []
r_id: int = 1
while POPULATION_NUM + 1 > r_id:
    for y in range(1, GRID_REC_SIZE + 1):
        if r_id >= POPULATION_NUM:
            break
        for x in range(1, GRID_REC_SIZE + 1):
            res = Resident.Resident(r_id, x, y)
            stay_at_home_population_list.append(res)

            stay_at_home_grid.get_cell(x, y).set_resident(r_id)

            r_id += 1
            if r_id >= POPULATION_NUM + 1:
                break

# infect one random resident and update its cell
r_id = random.randint(1, POPULATION_NUM + 1)
print(f"Infecting resident id: {r_id}")
resident = no_policy_population_list[r_id - 1]
resident.update_health_status(1)
stay_at_home_grid.get_cell(resident.cell_x, resident.cell_y).set_infected_resident(r_id)
stay_at_home_grid.get_cell(resident.cell_x, resident.cell_y).introduce_slf()

total_infected_counter = 1
total_recovered_counter = 0
total_currentsick_counter = 0
for t in range(1, TIME_STEPS):
    t_start = time.perf_counter()

    new_infected = infection_func(stay_at_home_population_list, stay_at_home_grid)
    new_recovered = recovery_func(stay_at_home_population_list, stay_at_home_grid, RECOVERY_TIME_STEPS)
    # print('t={:<6d} Infected={:<6d} Recovered={:<6d} Totals: Sicks:{:<6d} Recovers:{:<6d}'.format(t,new_infected,new_recovered,total_infected_counter,total_recovered_counter))
    travel_func(stay_at_home_population_list, stay_at_home_grid, STAY_AT_HOME_Policy)

    total_infected_counter += new_infected
    total_recovered_counter += new_recovered
    total_currentsick_counter = total_infected_counter - total_recovered_counter
    stay_at_home_policy_sick_list.append(total_currentsick_counter)

    print('t={:<6d} totalsick={:<6d}'.format(t, total_currentsick_counter))
    t_end = time.perf_counter()
    # print(f'Finished in {t_end-t_start} seconds')

##########################
# self quarantine Policy Simulation
##########################
# Create the Haifa Grid, with empty residents
self_quarantine_grid = Grid.Grid(GRID_REC_SIZE)

# Create list of ALL residents with:
# healthy status, uniform (even) distribution within the cells
# Add resident to its Cell
self_quarantine_population_list = []
r_id: int = 1
while POPULATION_NUM + 1 > r_id:
    for y in range(1, GRID_REC_SIZE + 1):
        if r_id >= POPULATION_NUM:
            break
        for x in range(1, GRID_REC_SIZE + 1):
            res = Resident.Resident(r_id, x, y)
            self_quarantine_population_list.append(res)

            self_quarantine_grid.get_cell(x, y).set_resident(r_id)

            r_id += 1
            if r_id >= POPULATION_NUM + 1:
                break

# infect one random resident and update its cell
r_id = random.randint(1, POPULATION_NUM + 1)
print(f"Infecting resident id: {r_id}")
resident = self_quarantine_population_list[r_id - 1]
resident.update_health_status(1)
self_quarantine_grid.get_cell(resident.cell_x, resident.cell_y).set_infected_resident(r_id)
self_quarantine_grid.get_cell(resident.cell_x, resident.cell_y).introduce_slf()

total_infected_counter = 1
total_recovered_counter = 0
total_currentsick_counter = 0
for t in range(1, TIME_STEPS):
    t_start = time.perf_counter()

    new_infected = 0
    new_infected = infection_func(self_quarantine_population_list, self_quarantine_grid)
    new_recovered = recovery_func(self_quarantine_population_list, self_quarantine_grid, RECOVERY_TIME_STEPS)
    # print('t={:<6d} Infected={:<6d} Recovered={:<6d} Totals: Sicks:{:<6d} Recovers:{:<6d}'.format(t,new_infected,new_recovered,total_infected_counter,total_recovered_counter))
    travel_func(self_quarantine_population_list, self_quarantine_grid, SELF_QUARANTINE_POLICY)

    total_infected_counter += new_infected
    total_recovered_counter += new_recovered
    total_currentsick_counter = total_infected_counter - total_recovered_counter
    self_quarantine_policy_sick_list.append(total_currentsick_counter)

    print('t={:<6d} totalsick={:<6d}'.format(t, total_currentsick_counter))
    t_end = time.perf_counter()
    # print(f'Finished in {t_end-t_start} seconds')

#==================================

Plots.plot_sick_func(no_policy_sick_list, stay_at_home_policy_sick_list, self_quarantine_policy_sick_list, TIME_STEPS)

#print(f"total Sicks {total_infected_counter}, total recovered {total_recovered_counter}")

####################### Testing Section #############
# for r in population_list:
#     r.introduce_slf()

# haifa_grid.get_cell(1,1).introduce_slf()
# haifa_grid.get_cell(1, 16).introduce_slf()
# haifa_grid.get_cell(16, 1).introduce_slf()
# haifa_grid.get_cell(16, 16).introduce_slf()

# infect one random resident and update its cell
# r_id = random.randrange(1, POPULATION_NUM+1)
# # r_id = 1
# print(f"Infecting resident id: {r_id}")
# res = population_list[r_id-1]
# res.update_health_status(1)
# haifa_grid.get_cell(res.cell_x, res.cell_y).set_infected_resident(r_id)
# haifa_grid.get_cell(res.cell_x, res.cell_y).introduce_slf()

#print("===================")

# Test our functions
# Functions.infection_func(population_list, haifa_grid)
# Functions.travel_func(population_list, haifa_grid, Q_PROB)
#
# haifa_grid.get_cell(res.cell_x, res.cell_y).introduce_slf()
#
#print("===================")
# pop_health_count = 0
# pop_sick_count = 0
# pop_recover_count = 0
# pop_health_count = Resident.calc_population_health_by_status(population_list, 0)
# pop_sick_count = Resident.calc_population_health_by_status(population_list, 1)
# pop_recover_count = Resident.calc_population_health_by_status(population_list, 2)
# print(f"Health count: {pop_health_count}")
# print(f"Sick count: {pop_sick_count}")
# print(f"Recover count: {pop_recover_count}")

