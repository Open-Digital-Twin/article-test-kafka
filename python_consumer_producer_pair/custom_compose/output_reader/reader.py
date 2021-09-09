import pandas as pd
from sys import argv, exit
import pathlib
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", help="File to be open", nargs='?', type=str)
# -k 2 -p 1 -c 2
parser.add_argument("-s", "--scale_loose", help="(0/1) If 1, the scale size of the graph will be defined by the highest value", nargs='?', const=False, type=bool, default=False)
parser.add_argument("-n", "--n_times", help="Runs experiment N times", nargs='?', const=1, type=int, default=1)

args = parser.parse_args()

# current_dir = str(getcwd())


file_path = str(pathlib.Path(__file__).parent.absolute())
file_path = file_path.replace('output_reader','')

file_to_open = args.file
loose_scales = args.scale_loose

panda_csv = pd.read_csv(file_path + file_to_open, skiprows= 1, usecols=[1,3,4,5,6], names=['kafka_timestamp', 'message_producer_time', 'message_consumer_time', 'consumer_produtor_latency', 'time_passed_since_kafka_timestamp_1'])

x = panda_csv.index
# cpu_perc = panda_csv['cpu_%'].str.replace('%', '')
# cpu_perc = pd.to_numeric(cpu_perc, downcast='float')

# mem_tmp2 = pd.DataFrame(panda_csv['mem_usage / limit'].str.split('/',1).tolist(),
#                                  columns = ['mem_usage','limit'], index = panda_csv.index)

# mem_usag = mem_tmp2['mem_usage'].str.replace('MiB', '')
# mem_usag = pd.to_numeric(mem_usag, downcast='float')

experiment_time = panda_csv['message_consumer_time'][panda_csv.index[-1]] - panda_csv['message_producer_time'][panda_csv.index[0]]
latency_mean = panda_csv['consumer_produtor_latency'].mean()
total_latency = panda_csv['consumer_produtor_latency'].sum()

# cpu_p_mean = cpu_perc.mean()

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

# color = 'tab:blue'
# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
# ax2.set_ylabel('time passed since first kafka timestamp (seconds)', color=color)  # we already handled the x-label with ax1
# if not loose_scales:
# 	plt.ylim([0, 20])
# ax2.plot(x, panda_csv['message_producer_time'], color=color, label=f'mean latency: {latency_mean.round(4)}')
# plt.legend(loc='center left')
# ax2.tick_params(axis='y', labelcolor=color)

graph.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

