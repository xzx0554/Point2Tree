import os
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
input_folder = '/examples'
output_folder = '/examples'
num_faces = pd.read_csv('/examples/example_mesh_num.csv')
os.makedirs(output_folder, exist_ok=True)

ply_files = [f for f in os.listdir(input_folder) if f.endswith('.ply')]
print(ply_files)
def convert_file(ply_file):
    input_path = os.path.join(input_folder, ply_file)
    output_file = ply_file.replace('.ply', '.obj')
    matching_rows = num_faces[num_faces['NewName'] == ply_file.replace('.ply', '')]
    if not matching_rows.empty:
        face_num = int(num_faces[num_faces['NewName']==ply_file.replace('.ply', '')]['TotalBranches'].values[0])
        output_path = os.path.join(output_folder, output_file)
        cmd = f"python ./convex_hull.py --i {input_path} --o {output_path} --faces {face_num} --manifold-path ./code/Manifold/build "
        print(cmd)
        subprocess.run(cmd,shell=True )
    else:
        print('ko')
    output_path = os.path.join(output_folder, output_file)
    cmd = f"python ./convex_hull.py --i {input_path} --o {output_path} --faces {face_num} --manifold-path ./code/Manifold/build "
    print(cmd)
    subprocess.run(cmd,shell=True )


with ThreadPoolExecutor(max_workers=12) as executor:
    list(tqdm(executor.map(convert_file, ply_files), total=len(ply_files), desc="Converting PLY to OBJ"))

print("Conversion completed.")
