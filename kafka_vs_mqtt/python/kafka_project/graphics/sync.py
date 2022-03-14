from numpy import append
import pandas as pd

def sanitize_docker_stats(file_to_open, exp_num, exp_type, home_dir = '/home/adbarros/'):
    import numpy as np
    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'

    panda_csv = pd.read_csv(file_path + 'csv/' + file_to_open, usecols=[1, 2, 3], names=['cpu_%', 'mem_usage / limit', 'NetI/O'])

    panda_csv.replace('', np.nan, inplace=True)
    panda_csv = panda_csv.dropna()

    panda_csv['cpu_%'] = panda_csv['cpu_%'].str.replace('%', '')
    panda_csv['cpu_%'] = pd.to_numeric(panda_csv['cpu_%'], downcast='float')

    net_io_tmp = pd.DataFrame(panda_csv['NetI/O'].str.split('/', 1).tolist(), columns=['Net In', 'Net Out'], index=panda_csv.index)
    panda_csv['net_in'], panda_csv['net_out'] = net_io_tmp['Net In'], net_io_tmp['Net Out']

    mem_temp = pd.DataFrame(panda_csv['mem_usage / limit'].str.split('/', 1).tolist(), columns=['mem_usage', 'limit'], index=panda_csv.index)
    panda_csv['mem_usage'] = mem_temp['mem_usage']
    # panda_csv['limit'] = mem_temp['limit']

    panda_csv.pop('mem_usage / limit')
    panda_csv.pop('NetI/O')

    panda_csv['net_in'] = panda_csv['net_in'].replace(
            {
                'B': '',
                'k': '*1e3', 
                'M': '*1e6',
                'G': '*1e9',  
                '-':'*-1'
            }, 
            regex=True
        ).map(pd.eval).astype(int)
    panda_csv['net_in'] = panda_csv['net_in'].div(1000000)

    panda_csv['net_out'] = panda_csv['net_out'].replace(
            {
                'B"': '',
                'k': '*1e3', 
                'M': '*1e6',
                'G': '*1e9',
                '-':'*-1'
            }, 
            regex=True
        ).map(pd.eval).astype(int)
    panda_csv['net_out'] = panda_csv['net_out'].div(1000000)

    panda_csv['mem_usage'] = panda_csv['mem_usage'].replace(
            {
                'B': '',
                'k': '*1e3', 
                'Mi': '*1e6', 
                'Gi': '*1e9', 
                '-':'*-1'
            }, 
            regex=True
        ).map(pd.eval).astype(int)
    panda_csv['mem_usage'] = panda_csv['mem_usage'].div(1000000)

    # panda_csv['limit'] = panda_csv['limit'].replace(
    #         {
    #             'B': '',
    #             'k': '*1e3', 
    #             'Mi': '*1e6', 
    #             'Gi': '*1e9', 
    #             '-':'*-1'
    #         }, 
    #         regex=True
    #     ).map(pd.eval).astype(int)
    # panda_csv['limit'] = panda_csv['limit'].div(1000000)

    panda_csv.to_csv(f'{file_path}csv/{file_to_open}', index=False)




def sync_consumer_out(file_ = '', time_zero = 0, exp_num = '', home_dir= '/home/adbarros/', exp_type = 'kafka'):
    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'

    panda_csv = pd.read_csv(f'{file_path}csv/{file_}', header = 0)

    first_message_time = panda_csv['message_producer_time'][0]

    panda_csv['message_producer_time'] -= first_message_time
    panda_csv['message_consumer_time'] -= first_message_time

    if time_zero > 0:
        panda_csv['message_producer_time'] += time_zero
        panda_csv['message_consumer_time'] += time_zero


    panda_csv.to_csv(f'{file_path}csv/relative_times/{file_}', index=False)


def join_results(file_list = [], exp_num = '', home_dir = '/home/adbarros/', exp_type = 'kafka', clear_csv = 'false'):
    from pathlib import Path

    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'
    new_df = pd.read_csv(f'{file_path}csv/relative_times/{file_list[0]}', header = 0)
    
    for file_ in file_list[1:]:
        try:
            linked_file = f'{file_path}csv/relative_times/{file_}'
            panda_csv = pd.read_csv(linked_file, header = 0)
            new_df = new_df.append(panda_csv, ignore_index = True)
        except Exception as e:
            print(str(e))
                
    new_df.sort_values(by=['message_producer_time'], inplace=True)
    new_df.to_csv(f'{file_path}csv/output_docker_complete', index=False)

    for file_ in file_list:
        linked_file = f'{file_path}csv/relative_times/{file_}'
        if (clear_csv == 'true'):
            tmp_file = Path(linked_file)
            try:
                tmp_file.unlink()
            except Exception as e:
                print(str(e))


def sum_docker_stats(machine, file_list, exp_num, home_dir, exp_type):

    file_path = f'{home_dir}{exp_type}_experiment_{exp_num}/'

    print(f'All files in {machine}: {file_list}')

    consumer_files = []
    for file_ in file_list:
        if ('consumer' in file_) and (machine in file_):
            consumer_files.append(file_)
    
    print(f'Consumer files for machine {machine}: {consumer_files}')

    consumer_df_sum = pd.read_csv(f'{file_path}csv/{consumer_files[0]}', header = 0)
    consumer_df_mean = pd.read_csv(f'{file_path}csv/{consumer_files[0]}', header = 0)

    for file_ in consumer_files[1:]:
        file_df = pd.read_csv(f'{file_path}csv/{file_}', header = 0)
        consumer_df_sum = consumer_df_sum.add(file_df, fill_value=0)
        consumer_df_mean = consumer_df_mean.mean(file_df, fill_value=0)

    consumer_df_mean.to_csv(f'{file_path}csv/docker_consumer_stats_mean_{machine}', index=False)
    consumer_df_sum.to_csv(f'{file_path}csv/docker_consumer_stats_sum_{machine}', index=False)

    producer_files = []
    for file_ in file_list:
        if ('producer' in file_) and (machine in file_):
            producer_files.append(file_)

    print(f'Producer files for machine {machine}: {producer_files}')

    producer_df_mean = pd.read_csv(f'{file_path}csv/{producer_files[0]}', header = 0)
    producer_df_mean = pd.read_csv(f'{file_path}csv/{producer_files[0]}', header = 0)
    for file_ in producer_files[1:]:
        file_df = pd.read_csv(f'{file_path}csv/{file_}', header = 0)
        producer_df_mean = producer_df_mean.add(file_df, fill_value=0)
        producer_df_mean = producer_df_mean.mean(file_df, fill_value=0)

    producer_df_mean.to_csv(f'{file_path}csv/docker_producer_stats_mean_{machine}', index=False)
    producer_df_mean.to_csv(f'{file_path}csv/docker_producer_stats_sum_{machine}', index=False)

    total_df = producer_df_mean.add(consumer_df_sum, fill_value=0)
    total_df.to_csv(f'{file_path}csv/docker_total_stats_sum_{machine}', index=False)

    return [f'docker_total_stats_sum_{machine}', f'docker_producer_stats_sum_{machine}', f'docker_consumer_stats_sum_{machine}', f'docker_producer_stats_mean_{machine}', f'docker_consumer_stats_mean_{machine}']

if __name__ == '__main__':
    # sync_consumer_out(time_zero= 60, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose_2.txt')
    # sync_consumer_out(time_zero= 30, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose_1.txt')
    # sync_consumer_out(time_zero= 0, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose.txt')
    # join_results(exp_num= 636668609, clear_csv='true', file_list=['output_docker_compose_2.txt','output_docker_compose_1.txt','output_docker_compose.txt'], home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/')

    sanitize_docker_stats(home_dir = '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_to_open = 'docker_stats_1111.txt', exp_num = '636668609', exp_type = 'kafka')