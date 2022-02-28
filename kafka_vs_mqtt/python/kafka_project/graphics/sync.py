import pandas as pd


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
    for file_ in file_list:
        linked_file = f'{file_path}csv/relative_times/{file_}'
        if (clear_csv == 'true'):
            tmp_file = Path(linked_file)
            try:
                tmp_file.unlink()
            except Exception as e:
                print(str(e))
                
    new_df.sort_values(by=['message_producer_time'], inplace=True)
    new_df.to_csv(f'{file_path}csv/output_docker_complete', index=False)

if __name__ == '__main__':
    sync_consumer_out(time_zero= 60, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose_2.txt')
    sync_consumer_out(time_zero= 30, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose_1.txt')
    sync_consumer_out(time_zero= 0, exp_num= 636668609, home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/', file_= 'output_docker_compose.txt')
    join_results(exp_num= 636668609, clear_csv='true', file_list=['output_docker_compose_2.txt','output_docker_compose_1.txt','output_docker_compose.txt'], home_dir= '/home/andreo/Dropbox/DropWorkspace/kafka/article-test-kafka/kafka_vs_mqtt/python/kafka_project/graphics/gitignore/')
