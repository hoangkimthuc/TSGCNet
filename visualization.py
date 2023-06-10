import numpy as np
import plotly.graph_objs as go
from plyfile import PlyData

def visualize(plyfile_path: str) -> None:
# Load the point cloud from the PLY file using PlyData
    plydata = PlyData.read(plyfile_path)

    # Extract the vertices, faces, and face colors as Numpy arrays
    vertices = np.array([plydata['vertex'][dimension] for dimension in ['x', 'y', 'z']]).T
    faces = np.concatenate(plydata['face']['vertex_indices'])

    colors = np.array([plydata['face'][color] for color in ['red', 'green', 'blue']]).T / 255.0

    # Reshape the faces array into a (n_faces, 3) array
    faces = faces.reshape((-1, 3))

    # Create a 3D scatter plot of the vertices and faces
    fig = go.Figure()
    # fig.add_trace(go.Scatter3d(x=vertices[:,0], y=vertices[:,1], z=vertices[:,2], mode='markers', 
                            #    marker=dict(size=2, color='black')))
    fig.add_trace(go.Mesh3d(x=vertices[:,0], y=vertices[:,1], z=vertices[:,2], 
                            i=faces[:,0], j=faces[:,1], k=faces[:,2], 
                            facecolor=colors))

    # Set the axis titles and display the plot
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
    fig.show()
if __name__ == '__main__':
    
    visualize('output/output_1.ply')