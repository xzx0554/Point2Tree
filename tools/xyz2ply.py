import os
import pandas as pd
import open3d as o3d
import numpy as np

def csv_to_ply(csv_path, ply_path, search_param=o3d.geometry.KDTreeSearchParamKNN(knn=30)):
    print(csv_path)
    df = pd.read_csv(csv_path, header=None, sep=' ')
    
    if df.shape[1] < 3:
        print(f"File {csv_path} has fewer than 3 columns - cannot extract x,y,z coordinates. Skipping.")
        return
    
    points = df.iloc[:, :3].values.astype(np.float32)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals(search_param=search_param)
    pcd.normalize_normals()  
    normals = np.asarray(pcd.normals)
    vertex_count = points.shape[0]
    header = f'''ply
format ascii 1.0
comment Created by csv_to_ply_with_normals_script
element vertex {vertex_count}
property float x
property float y
property float z
property float nx
property float ny
property float nz
end_header
'''
    data = "\n".join([
        f"{points[i,0]} {points[i,1]} {points[i,2]} {normals[i,0]} {normals[i,1]} {normals[i,2]}"
        for i in range(vertex_count)
    ])
    
    with open(ply_path, 'w') as ply_file:
        ply_file.write(header)
        ply_file.write(data)
    

def convert_all_csv_to_ply(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.xyz'):
            csv_path = os.path.join(folder_path, filename)
            ply_filename = os.path.splitext(filename)[0] + '.ply'
            ply_path = os.path.join(folder_path, ply_filename)
            csv_to_ply(csv_path, ply_path)
    

if __name__ == "__main__":
    folder_path = '/examples'  
    
    if not os.path.isdir(folder_path):
        print(f"dir {folder_path} not exist.Please check if the root is right。")
    else:
        convert_all_csv_to_ply(folder_path)

