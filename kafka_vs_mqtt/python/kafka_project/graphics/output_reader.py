import pandas as pd
from os import makedirs

# from auxiliaryfunctions.terminal import print_centralized

def create_message_graph(exp_num = '', file_to_open = '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/', clear_csv = 'false', exp_type = 'kafka'):
    # print_centralized(' Creating Message Graph ')

    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'

    panda_csv = pd.read_csv(f'{file_path}csv/{file_to_open}', header = 0)
    csv_header = panda_csv.index

    experiment_time = panda_csv['message_consumer_time'].iloc[-1] - panda_csv['message_producer_time'][0]
    time_elapsed_for_kafka = panda_csv['kafka_timestamp'].iloc[-1] - panda_csv['kafka_timestamp'][0] if 'kafka_timestamp' in panda_csv.columns else False
    latencies = panda_csv['message_consumer_time'] - panda_csv['message_producer_time']

    import matplotlib.pyplot as plt
    plt.rcParams['axes.facecolor'] = (0.5,0.5,0.5,0.5)
    plt.rcParams['figure.facecolor'] = (1,1,1,0.8)
    
    graph, ax1 = plt.subplots()

    color = 'tab:green'
    ax1.set_xlabel('number of measures')
    if not loose_scales:
        plt.ylim([0, 0.5])
    
    ax1.set_ylabel('Latency (seconds)', color=color)

    ax1.plot(
        csv_header, latencies, color = color,
        label = \
            f'{"Timelapse kafka stamps: " + str(time_elapsed_for_kafka.round(6)) if time_elapsed_for_kafka else ""} \n' +
            f'Experiment timelapse: {experiment_time.round(6)}\n' +
            f'Mean latency: {latencies.mean().round(6)}\n' +
            f'First latency: {latencies[0].round(6)}\n' +
            f'Last latency: {latencies.iloc[-1].round(6)}\n' +
            f'Message size: {panda_csv["message_size"][0]} :: ' +
            f'Package size: {panda_csv["total_size"][0]}'
    )

    plt.legend(loc='upper right')
    plt.grid(True, color = 'grey')

    ax1.tick_params(axis = 'y', labelcolor = color)

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
        # print_centralized(' Removing csv folder ')
        from pathlib import Path
        tmp_file = Path(file_path + 'csv/' + file_to_open)
        tmp_file.unlink()

    # print_centralized(' End ')

if __name__ == '__main__':
    create_message_graph(exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_to_open= 'output_docker_compose.txt', save_image= 'output_docker_compose.png')
