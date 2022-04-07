import pandas as pd
import numpy as np
from os import makedirs

# from auxiliaryfunctions.terminal import print_centralized

def create_stats_graph(exp_num= '', file_to_open= '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/', home_folder = '', exp_type = 'kafka', clear_csv = 'false'):
    # print_centralized(f' Creating stats graph for: {file_to_open} ')

    file_path = f'{home_folder}/{home_dir}{exp_type}_experiment_{exp_num}/'
    file_to_save = save_image

    panda_csv = pd.read_csv(file_path + 'csv/' + file_to_open, header=0)

    panda_csv.replace('', np.nan, inplace=True)
    panda_csv = panda_csv.dropna()

    x = panda_csv.index

    mem_total = panda_csv['mem_usage'].iloc[-1] - panda_csv['mem_usage'][0]
    net_out_total = panda_csv['net_out'].iloc[-1] - panda_csv['net_out'][0]
    net_in_total = panda_csv['net_in'].iloc[-1] - panda_csv['net_in'][0]

    usage_mean = panda_csv['mem_usage'].max()
    cpu_p_mean = panda_csv['cpu_%'].mean()

    # once the file is open, we create the graph
    import matplotlib.pyplot as plt
    plt.rcParams['axes.facecolor'] = (0.5,0.5,0.5,0.5)
    plt.rcParams['figure.facecolor'] = (1,1,1,0.8)
    
    graph, ax1 = plt.subplots(2)

    color = 'tab:orange'
    ax1[0].set_xlabel('number of measures')

    if not loose_scales:
        plt.ylim([0, 600])

    ax1[0].set_ylabel('memory usage (MiB)', color=color)
    ax1[0].plot(
        x, panda_csv['mem_usage'], color=color, 
        label=f'Max memory usage: {int(usage_mean*100)/100}\n' + \
            f'Total memory: {mem_total}\n' + \
            f'Total net in: {net_out_total}\n' + \
            f'Total net out: {net_in_total}'
        )
    ax1[0].legend(loc='upper left', bbox_to_anchor=[-0.0001, 0.83])
    ax1[0].tick_params(axis='y', labelcolor=color)

    color = 'tab:blue'
    ax2 = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('cpu percentage (%)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    
    ax2.plot(x, panda_csv['cpu_%'], color=color, label=f'Mean processor usage: {int(cpu_p_mean*100)/100}')
    ax2.legend(loc='upper left')
    ax2.tick_params(axis='y', labelcolor=color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    color = 'tab:green'

    ax1[1].set_ylabel('Net In (MB)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    ax1[1].plot(x, panda_csv['net_in'], color=color)
    ax1[1].tick_params(axis='y')

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    color = 'tab:red'
    ax4 = ax1[1].twinx()  # instantiate a second axes that shares the same x-axis
    ax4.set_ylabel('Net Out (MB)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    ax4.plot(x, panda_csv['net_out'], color=color)
    ax4.tick_params(axis='y')
            

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    file_to_print = file_to_save
    file_to_print = file_to_print.strip()

    target_folder = 'graphs/'
    if 'consumer' in file_to_open:
        target_folder = target_folder + 'consumer/'
    elif 'producer' in file_to_open:
        target_folder = target_folder + 'producer/'
    elif 'docker' in file_to_open:
        target_folder = target_folder + 'docker_nodes/'

    makedirs(file_path + target_folder, exist_ok = True)
    out = str(file_path + target_folder + file_to_print)

    file_type = file_to_print.split('.')[-1]
    print(f'"{out}"')
    plt.savefig(out, format = file_type)
    plt.close()

    if (clear_csv == 'true'):
        # print_centralized(' Removing csv folder ')
        from pathlib import Path
        tmp_file = Path(file_path + 'csv/' + file_to_open)
        tmp_file.unlink()

    # print_centralized(' End ')

if __name__ == '__main__':
    print(create_stats_graph(exp_num = 636668609, home_folder = 'gitignore', file_to_open = 'docker_stats_1111.txt', save_image = 'docker_stats_1111.txt.svg', home_dir = ''))
