import pandas as pd
from os import makedirs

# from auxiliaryfunctions.terminal import print_centralized


def smooth2(scalars, weight, mean_latency):  # Weight between 0 and 1
    low_value_start = (mean_latency * weight) + ((1 - weight) * scalars[0]) 
    smoothed = [low_value_start]
    for position, point in enumerate(scalars[1:], start=1):
        smoothed_val = (smoothed[position-1] * weight) + ((1 - weight) * point)
        # if smoothed_val > mean_latency: 
        #     smoothed_val = (mean_latency * weight) + ((1 - weight) * smoothed_val)
        # if smoothed_val < mean_latency: 
        #     smoothed_val = (mean_latency * weight) + ((1 - weight) * smoothed_val)
        smoothed.append(smoothed_val)                      



    return smoothed


def create_message_graph(exp_num = '', file_to_open = '', loose_scales= True, save_image= '', home_dir= '/home/adbarros/', clear_csv = 'false', exp_type = 'kafka', expected_complete_num = 0):
    # print_centralized(' Creating Message Graph ')

    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'

    panda_csv = pd.read_csv(f'{file_path}csv/{file_to_open}', header = 0)
    csv_header = panda_csv.index

    mean_producer_msg_latency = panda_csv['message_producer_time'].diff().mean()
    producer_lifetime = panda_csv['message_producer_time'].iloc[-1] - panda_csv['message_producer_time'][0]
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

    labels = \
            f'Experiment timelapse: {experiment_time.round(6)}\n' + \
            f'Producer lifetime:{producer_lifetime.round(6)}\n' + \
            f'Mean producer latency {mean_producer_msg_latency.round(6)}\n' + \
            f'Mean message latency: {latencies.mean().round(6)}\n' + \
            f'First message latency: {latencies[0].round(6)}\n' + \
            f'Last message latency: {latencies.iloc[-1].round(6)}\n' + \
            f'Message size: {panda_csv["message_size"][0]} :: ' + \
            f'Package size: {panda_csv["total_size"][0]}'

    if (len(latencies) < expected_complete_num) and 'complete' in file_to_open:
        labels + f'\nMissing amount of messages: {expected_complete_num - len(latencies)}'

    timelapse_kafka = "Timelapse kafka stamps: " + str(time_elapsed_for_kafka.round(6)) + "\n" if time_elapsed_for_kafka else ""
    ax1.plot(
        panda_csv['message_consumer_time'], latencies, color = color,
        label = \
            f'{timelapse_kafka}' + labels
    )

    plt.legend(loc='upper right')
    plt.grid(True, color = 'grey')

    ax1.tick_params(axis = 'y', labelcolor = color)

    graph.tight_layout()  # otherwise the right y-label is slightly clipped
    if len(save_image) > 0:
        file_to_print = str(save_image)
        file_to_print = file_to_print.strip()

        target_folder = 'graphs/'
        if 'out_dtwins' in file_to_open:
            target_folder = target_folder + 'dtwins_out/'

        makedirs(file_path + target_folder, exist_ok = True)
        out = str(file_path + target_folder + file_to_print)
        print(f'"{out}"')

        file_type = file_to_print.split('.')[-1]
        plt.savefig(out, format=file_type)

        # create smooth graph
        # from scipy.interpolate import interp1d
        # import numpy as np 
        ax1.clear()
        mean_latency=latencies.mean().round(6)
        
        numbers = smooth2(scalars=latencies, weight=.7, mean_latency=mean_latency)
        # print(max(numbers))
        plt.ylim([0, 5*mean_latency])
        # cubic_interploation_model = interp1d(range(len(numbers)), numbers, kind = "cubic")
        
        # Plotting the Graph
        # X_=np.linspace(1, len(numbers)-1, 150)
        # Y_=cubic_interploation_model(X_)

        print(labels)
        ax1.plot(
            numbers,         
            label = \
                f'{timelapse_kafka}' + labels
        )

        plt.savefig(f'{out}_smooth.{file_type}', format=file_type)

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
    create_message_graph(exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_to_open= 'output_docker_complete', save_image= 'output_docker_complete.png')
