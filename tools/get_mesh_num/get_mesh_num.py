import subprocess
import re
import os
from tqdm import tqdm
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import concurrent
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_str = result.stdout.decode()
    except subprocess.CalledProcessError as e:
        output_str = e.output.decode()
        print(output_str)
    
    match = re.search(r"Total number of branches: (\d+)", output_str)
    if match:
        total_branches = int(match.group(1))
        return total_branches
    else:
        print("Branch count not found in the output.")
        return None

def process_file(file_name):
    command = os.path.join(xyz_folder, file_name)
    print('./AdTree' + ' ' + command)
    total_branches = run_command('./AdTree' + ' ' + command + ' cache_AdTree')
    
    return {'name': file_name.replace('.xyz', ''), 'total_branches': total_branches}

file_name_list = []
columns = ['name', 'total_branches']
xyz_folder = '/examples'

with ThreadPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(process_file, file_name) for file_name in os.listdir(xyz_folder) if file_name.endswith('.xyz')]
    for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
        file_name_list.append(future.result())

df = pd.DataFrame(file_name_list, columns=columns)
df.to_csv('/examples/example_mesh_num.csv',index=False)
