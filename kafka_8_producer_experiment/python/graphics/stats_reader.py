import pandas as pd
from os import makedirs

from auxiliaryfunctions.terminal import print_centralized

def create_stats_graph(exp_num= '', file_to_open= '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/'):
    print_centralized(f' Creating stats graph for: {file_to_open} ')

    file_path = f'{home_dir}experiment_{exp_num}/'
    file_to_save = save_image

    panda_csv = pd.read_csv(file_path + 'csv/' + file_to_open, usecols=[1,2], names=['cpu_%', 'mem_usage / limit'])

    x = panda_csv.index
    cpu_perc = panda_csv['cpu_%'].str.replace('%', '')
    cpu_perc = pd.to_numeric(cpu_perc, downcast='float')

    mem_tmp2 = pd.DataFrame(panda_csv['mem_usage / limit'].str.split('/',1).tolist(),
                                        columns = ['mem_usage','limit'], index = panda_csv.index)


    mem_tmp2['mem_usage'] = mem_tmp2['mem_usage'].str.replace('GiB', '')
    mem_usag = mem_tmp2['mem_usage'].str.replace('MiB', '')

    mem_usag = pd.to_numeric(mem_usag, downcast='float')

    usage_mean = mem_usag.mean()
    cpu_p_mean = cpu_perc.mean()

    # once the file is open, we create the graph
    import matplotlib.pyplot as plt

    graph, ax1 = plt.subplots()

    color = 'tab:orange'
    ax1.set_xlabel('number of measures')

    if not loose_scales:
        plt.ylim([0, 600])

    ax1.set_ylabel('memory usage (MiB)', color=color)
    ax1.plot(x, mem_usag, color=color, label=f'mean memory usage: {round(usage_mean, 4)}')
    plt.legend(loc='upper left')
    ax1.tick_params(axis='y', labelcolor=color)

    color = 'tab:blue'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('cpu percentage (%)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
            
    ax2.plot(x, cpu_perc, color=color, label=f'mean processor usage: {round(cpu_p_mean, 4)}')
    plt.legend(loc='center left')
    ax2.tick_params(axis='y', labelcolor=color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    file_to_print = file_to_save
    file_to_print = file_to_print.strip()

    makedirs(file_path + 'graphs/', exist_ok = True)
    out = str(file_path + 'graphs/' + file_to_print)

    file_type = file_to_print.split('.')[-1]
    print(f'"{out}"')
    plt.savefig(out, format= file_type)
    plt.close()

    print_centralized(' End ')

if __name__ == '__main__':
    print(create_stats_graph(exp_num= 636668609, file_to_open= 'docker_stats_4cbf7ab2b0a3.txt', save_image= 'docker_stats_4cbf7ab2b0a3.txt.svg'))
