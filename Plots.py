from matplotlib import pyplot as plt
from typing import List


def plot_sick_func(no_policy_sick_list: List, stay_at_home_policy_sick_list: List,
                   self_quarantine_sick_list: List, red_zone_policy_list: List, timesteps):
    t = []
    for i in range(1, timesteps):
        t.append(i)

    #ploting the points
    plt.plot(t, no_policy_sick_list, label='NO Policy')
    plt.plot(t, stay_at_home_policy_sick_list, label='Stay AT Home')
    plt.plot(t, self_quarantine_sick_list, label='Self Quarantine')
    plt.plot(t, red_zone_policy_list, label='RED Zones')
    #plt.plot(t, sick_list, color='green',linestyle='dashed',linewidth=3,marker='o',markerfacecolor='blue',markersize=12)

    #labels
    plt.xlabel('time steps')
    plt.ylabel('sick number')
    #title
    plt.title('sick people over time steps')
    plt.tight_layout()

    plt.legend()

    plt.savefig('Sick.png')

    # show the plot
    plt.show()