import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button, TextBox

#cubelets vertices
def create_unit_cube(offset):
    vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ]) + offset
    return vertices

#cubelets faces
def create_faces(vertices):
    faces = [
        [vertices[j] for j in [0, 1, 5, 4]],
        [vertices[j] for j in [7, 6, 2, 3]],
        [vertices[j] for j in [0, 3, 7, 4]],
        [vertices[j] for j in [1, 2, 6, 5]],
        [vertices[j] for j in [0, 1, 2, 3]],
        [vertices[j] for j in [4, 5, 6, 7]]
    ]
    return faces

#draw cubelets
def draw_cubes(ax, vertices_list, colors):
    for vertices, color in zip(vertices_list, colors):
        faces = create_faces(vertices)
        ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.75))

def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def draw_ground(ax):
    x = np.linspace(-1, 5, 2)
    y = np.linspace(-1, 5, 2)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    ax.plot_surface(X, Y, Z, color='gray', alpha=0.3)

#more visibility, in order to not let the cube go outside the scope
def update_cubes(ax, vertices_list, colors):
    ax.cla()
    draw_cubes(ax, vertices_list, colors)
    draw_ground(ax)
    ax.set_xlim([-1, 5])
    ax.set_ylim([-1, 5])
    ax.set_zlim([-1, 5])
    plt.draw()

#gets the avg of the whole cube
def get_global_center(vertices_list):
    all_points = np.vstack(vertices_list) # puts one on top of the other the rows, impiles one over each other, they have to be the same dim
    return np.mean(all_points, axis=0)

#rotation function on click
def rotate(event, axis, angle, ax, colors):
    global global_vertices_list, current_rotation_matrix
    if axis == 'x':
        R = rotation_matrix_x(angle)
    elif axis == 'y':
        R = rotation_matrix_y(angle)
    elif axis == 'z':
        R = rotation_matrix_z(angle)
    else:
        return
    
    center = get_global_center(global_vertices_list)

    #rotates cubelets around center
    new_vertices = []
    for v in global_vertices_list:
        rotated = np.dot(v - center, R.T) + center
        new_vertices.append(rotated)

    global_vertices_list = new_vertices
    update_cubes(ax, global_vertices_list, colors)

#cube translate adding what's insiede the textboxes
def update_position(ax, event=None):
    global global_vertices_list, offsets
    try:
        tx = float(text_box_x.text)
        ty = float(text_box_y.text)
        tz = float(text_box_z.text)
        translation = np.array([tx, ty, tz])

        #center = np.array([float(text_box_x.text), float(text_box_y.text), float(text_box_z.text)])
        global_vertices_list = [v + translation for v in global_vertices_list]

        update_cubes(ax, global_vertices_list, colors)
    except ValueError:
        pass  

def validate_positions(ax):
    global global_vertices_list

    invalid_cubes = []
    for i, vertices in enumerate(global_vertices_list):
        if np.any(vertices[:, 2] < 0):
            invalid_cubes.append(i)

    if invalid_cubes:
        print(f"not ok")
        temp_colors = colors.copy()
        for idx in invalid_cubes:
            temp_colors[idx] = 'red'
        update_cubes(ax, global_vertices_list, temp_colors)
    else:
        print("ok")
        update_cubes(ax, global_vertices_list, colors)


def main():
    global global_vertices_list, offsets, colors, text_box_x, text_box_y, text_box_z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #little cubelets
    offsets = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)]
    colors = ['grey', 'blue', 'orange', 'green']

    global_vertices_list = [create_unit_cube(offset) for offset in offsets]

    update_cubes(ax, global_vertices_list, colors)

    ax_box_x = plt.axes([0.2, 0.15, 0.1, 0.05])
    text_box_x = TextBox(ax_box_x, 'X', initial="0")

    ax_box_y = plt.axes([0.35, 0.15, 0.1, 0.05])
    text_box_y = TextBox(ax_box_y, 'Y', initial="0")

    ax_box_z = plt.axes([0.5, 0.15, 0.1, 0.05])
    text_box_z = TextBox(ax_box_z, 'Z', initial="0")

    text_box_x.on_text_change(lambda val: update_position(ax))
    text_box_y.on_text_change(lambda val: update_position(ax))
    text_box_z.on_text_change(lambda val: update_position(ax))

    #buttons for rotation
    ax_rot_x_90 = plt.axes([0.07, 0.01, 0.1, 0.075])
    btn_rot_x_90 = Button(ax_rot_x_90, 'Rotate X 90')

    ax_rot_y_90 = plt.axes([0.33, 0.01, 0.1, 0.075])
    btn_rot_y_90 = Button(ax_rot_y_90, 'Rotate Y 90')

    ax_rot_z_90 = plt.axes([0.60, 0.01, 0.1, 0.075])
    btn_rot_z_90 = Button(ax_rot_z_90, 'Rotate Z 90')

    ax_val_cube = plt.axes([0.85, 0.01, 0.1, 0.075])
    btn_val_cube = Button(ax_val_cube, "Check rot/pos")

    btn_rot_x_90.on_clicked(lambda event: rotate(event, 'x', np.pi/2, ax, colors))
    btn_rot_y_90.on_clicked(lambda event: rotate(event, 'y', np.pi/2, ax, colors))
    btn_rot_z_90.on_clicked(lambda event: rotate(event, 'z', np.pi/2, ax, colors))
    btn_val_cube.on_clicked(lambda event: validate_positions(ax))


    plt.show()

if __name__ == "__main__":
    main()
