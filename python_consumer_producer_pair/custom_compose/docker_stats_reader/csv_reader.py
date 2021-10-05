import pandas as pd

def save_stats_graph(file_path, file_to_open, file_to_save, loose_scales):
    file_path = f'{file_path}/'
    panda_csv = pd.read_csv(file_path + file_to_open, usecols=[1,2], names=['cpu_%', 'mem_usage / limit'])

    x = panda_csv.index
    cpu_perc = panda_csv['cpu_%'].str.replace('%', '')
    cpu_perc = pd.to_numeric(cpu_perc, downcast='float')

    mem_tmp2 = pd.DataFrame(panda_csv['mem_usage / limit'].str.split('/',1).tolist(),
                                    columns = ['mem_usage','limit'], index = panda_csv.index)

    mem_usag = mem_tmp2['mem_usage'].str.replace('GiB', '')
    mem_usag = mem_usag.replace('MiB', '')
    mem_usag = pd.to_numeric(mem_usag, downcast='float')

    usage_mean = mem_usag.mean()
    cpu_p_mean = cpu_perc.mean()

    # once the file is open, we create the graph
    import matplotlib.pyplot as plt

    graph, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel('number of measures')
    if not loose_scales:
        plt.ylim([0, 600])
    ax1.set_ylabel('memory usage (MiB)', color=color)
    ax1.plot(x, mem_usag, color=color, label=f'mean memory usage: {usage_mean.round(4)}')
    plt.legend(loc='upper left')
    ax1.tick_params(axis='y', labelcolor=color)

    color = 'tab:blue'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('cpu percentage (%)', color=color)  # we already handled the x-label with ax1
    if not loose_scales:
        plt.ylim([0, 100])
    ax2.plot(x, cpu_perc, color=color, label=f'mean processor usage: {cpu_p_mean.round(4)}')
    plt.legend(loc='center left')
    ax2.tick_params(axis='y', labelcolor=color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped

    file_to_print = file_to_save
    file_to_print = file_to_print.strip()
    out = str(file_path+file_to_print)
    print(f'"{out}"')
    plt.savefig(out)
    plt.close()
