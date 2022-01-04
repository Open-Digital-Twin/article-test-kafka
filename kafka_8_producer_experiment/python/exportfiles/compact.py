import subprocess
from time import sleep

def tar_experiment_dir(exp_number= '', home_dir= '/home/adbarros/'):
    exp_folder = f'experiment_{exp_number}'
    #tar_cmd = ['tar', '-cf', f'{home_dir}{exp_folder}.tar', f'{home_dir}{exp_folder}']
    tar_cmd = ['tar', '-C', f'{home_dir}', '-cvf', f'{home_dir}{exp_folder}.tar', f'{exp_folder}']
    print(f'Packing files into {exp_folder}.tar')
    subprocess.run(tar_cmd)

    sleep(2)
    return f'{home_dir}{exp_folder}.tar'

if __name__ == '__main__':
    print(tar_experiment_dir(921074387))

