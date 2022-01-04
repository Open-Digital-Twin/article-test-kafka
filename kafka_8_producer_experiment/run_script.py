import subprocess

producer_virtual_machines = ['dtwins5', 'dtwins6', 'dtwins7']

kafka_virtual_machines = ['dtwins', 'dtwins6', 'dtwins7']


docker_stats = subprocess.run(['docker', '-H dtwins2', 'stats', '--format', '"{{.Container}}, {{.CPUPerc}}, {{.MemUsage}}, {{.NetIO}}"'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, capture_output=True)
