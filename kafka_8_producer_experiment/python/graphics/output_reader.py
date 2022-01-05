import pandas as pd
from os import makedirs

from auxiliaryfunctions.terminal import print_centralized

def create_message_graph(exp_num = '', file_to_open = '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/', clear_csv = 'false'):
    print_centralized(' Creating Message Graph ')

    file_path = f'{home_dir}experiment_{exp_num}/'

    panda_csv = pd.read_csv(file_path + 'csv/' + file_to_open, skiprows= 1, usecols=[1,3,4,5,6], names=['kafka_timestamp', 'message_producer_time', 'message_consumer_time', 'consumer_produtor_latency', 'time_passed_since_kafka_timestamp_1'])

    x = panda_csv.index

    experiment_time = panda_csv['message_consumer_time'][panda_csv.index[-1]] - panda_csv['message_producer_time'][panda_csv.index[0]]
    latency_mean = panda_csv['consumer_produtor_latency'].mean()
    total_latency = panda_csv['consumer_produtor_latency'].sum()

    # once the file is open, we create the graph
    import matplotlib.pyplot as plt

    graph, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel('number of measures')
    if not loose_scales:
        plt.ylim([0, 0.5])
    
    ax1.set_ylabel('Latency (seconds)', color=color)

    ax1.plot(x, panda_csv['consumer_produtor_latency'], color=color,
            label=f"""Mean latency (seconds): {latency_mean.round(4)}
            Total latency (seconds): {total_latency}
            Time passed since first kafka timestamp (seconds): {panda_csv['time_passed_since_kafka_timestamp_1'][panda_csv.index[-1]]}
            First latency {panda_csv['consumer_produtor_latency'][panda_csv.index[0]]}
            Last latency {panda_csv['consumer_produtor_latency'][panda_csv.index[-1]]}
            Experiment timelapse {experiment_time}""")

    plt.legend(loc='upper right')
    ax1.tick_params(axis='y', labelcolor=color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped
    if len(save_image) > 0:
        file_to_print = str(save_image)
        file_to_print = file_to_print.strip()

        makedirs(file_path + 'graphs/', exist_ok = True)
        out = str(file_path + 'graphs/' + file_to_print)
        print(f'"{out}"')

        file_type = file_to_print.split('.')[-1]
        plt.savefig(out, format=file_type)
        plt.close()
    else:
        plt.show()

    if (clear_csv == 'true'):
        print_centralized(' Removing csv folder ')
        from pathlib import Path
        tmp_file = Path(file_path + 'csv/' + file_to_open)
        tmp_file.unlink(missing_ok = True)

    print_centralized(' End ')

if __name__ == '__main__':
    create_message_graph(exp_num= 636668609, file_to_open= 'out_dtwins6_c5066011a856_636668609', save_image= 'out_dtwins6_c5066011a856_636668609.png')
