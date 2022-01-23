import pandas as pd
import numpy as np
from os import makedirs

from auxiliaryfunctions.terminal import print_centralized

def create_stats_graph(exp_num= '', file_to_open= '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/', home_folder = '', exp_type = 'kafka'):
    print_centralized(f' Creating stats graph for: {file_to_open} ')

    file_path = f'{home_folder}/{home_dir}{exp_type}_experiment_{exp_num}/'
    file_to_save = save_image

    panda_csv = pd.read_csv(file_path + 'csv/' + file_to_open, usecols=[1,2,3], names=['cpu_%', 'mem_usage / limit', 'NetI/O'])

    panda_csv.replace('', np.nan, inplace=True)
    panda_csv = panda_csv.dropna()


    x = panda_csv.index
    cpu_perc = panda_csv['cpu_%'].str.replace('%', '')
    cpu_perc = pd.to_numeric(cpu_perc, downcast='float')

    net_io_tmp = pd.DataFrame(panda_csv['NetI/O'].str.split('/', 1).tolist(),
                                        columns = ['Net In', 'Net Out'], index = panda_csv.index)

    mem_tmp2 = pd.DataFrame(panda_csv['mem_usage / limit'].str.split('/', 1).tolist(),
                                        columns = ['mem_usage', 'limit'], index = panda_csv.index)


    net_in = net_io_tmp['Net In'].str.replace('kB', '')
    net_in = net_in.str.replace('MB', '')
    net_in = net_in.str.replace('B', '')
    net_in = net_in.str.replace('"', '')
    net_in = pd.to_numeric(net_in, downcast='float')

    net_out = net_io_tmp['Net Out'].str.replace('kB', '')
    net_out = net_out.str.replace('MB', '')
    net_out = net_out.str.replace('B', '')
    net_out = net_out.str.replace('"', '')
    net_out = pd.to_numeric(net_out, downcast='float')

    mem_usag = mem_tmp2['mem_usage'].str.replace('MiB', '')
    mem_tmp2['mem_usage'] = mem_tmp2['mem_usage'].str.replace('GiB', '')
    mem_usag = mem_tmp2['mem_usage'].str.replace('MiB', '')

    mem_usag = pd.to_numeric(mem_usag, downcast='float')

    usage_mean = mem_usag.max()
    cpu_p_mean = cpu_perc.mean()

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
    ax1[0].plot(x, mem_usag, color=color, label=f'Max memory usage: {round(usage_mean, 4)}')
    plt.legend(loc='upper right')
    ax1[0].tick_params(axis='y', labelcolor=color)

    color = 'tab:blue'
    ax2 = ax1[0].twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('cpu percentage (%)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
            
    ax2.plot(x, cpu_perc, color=color, label=f'mean processor usage: {round(cpu_p_mean, 4)}')
    plt.legend(loc='upper left')
    ax2.tick_params(axis='y', labelcolor=color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    color = 'tab:green'

    ax1[1].set_ylabel('Net In (kB -> MB)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    ax1[1].plot(x, net_in, color=color)
    ax1[1].tick_params(axis='y')

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    color = 'tab:red'
    ax4 = ax1[1].twinx()  # instantiate a second axes that shares the same x-axis
    ax4.set_ylabel('Net Out (kB -> MB)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    ax4.plot(x, net_out, color=color)
    ax4.tick_params(axis='y')
            

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    file_to_print = file_to_save
    file_to_print = file_to_print.strip()

    makedirs(file_path + 'graphs/', exist_ok = True)
    out = str(file_path + 'graphs/' + file_to_print)

    file_type = file_to_print.split('.')[-1]
    print(f'"{out}"')
    plt.savefig(out, format = file_type)
    plt.close()

    print_centralized(' End ')

if __name__ == '__main__':
    print(create_stats_graph(exp_num = 636668609, home_folder = 'gitignore', file_to_open = 'docker_stats_88f30141698f.txt', save_image = 'docker_stats_88f30141698f.txt.svg', home_dir = ''))
