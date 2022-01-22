import subprocess
from time import sleep

from auxiliaryfunctions.terminal import print_centralized

def tar_experiment_dir(exp_number= '', home_dir= '/home/adbarros/', exp_type = 'kafka'):
    exp_folder = f'{exp_type}_experiment_{exp_number}'
    print_centralized(f' Packing into {home_dir}{exp_folder}.tar ')

    tar_cmd = ['tar', '-C', f'{home_dir}', '-cvf', f'{home_dir}{exp_folder}.tar', f'{exp_folder}']
    print(f'Packing files into {exp_folder}.tar')
    subprocess.run(tar_cmd)

    sleep(1)

    print_centralized(' End ')
    return f'{home_dir}{exp_folder}.tar'

if __name__ == '__main__':
    print(tar_experiment_dir(921074387))

