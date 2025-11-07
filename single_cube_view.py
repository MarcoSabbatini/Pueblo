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

#related to center
def get_vertices_from_positions(cube_positions, center):
    vertices_list = []
    for pos in cube_positions:
        offset = center + pos
        vertices_list.append(create_unit_cube(offset))
    return vertices_list

def translate_center(center, direction):
    return center + direction

#vertices updated globally
def translate(ax, direction):
    global center, cube_positions, colors, global_vertices_list
    center = translate_center(center, direction)
    global_vertices_list = get_vertices_from_positions(cube_positions, center)
    update_cubes(ax, global_vertices_list, colors)

#k may be used better, rotates by 90 around x/y/z axis passing in the center
def rotate_positions(cube_positions, axis, k=1):

    R_x = np.array([[1, 0, 0],
                    [0, 0, -1],
                    [0, 1, 0]], dtype=int)
    R_y = np.array([[0, 0, 1],
                    [0, 1, 0],
                    [-1, 0, 0]], dtype=int)
    R_z = np.array([[0, -1, 0],
                    [1,  0, 0],
                    [0,  0, 1]], dtype=int)

    if axis == 'x':
        R = R_x
    elif axis == 'y':
        R = R_y
    elif axis == 'z':
        R = R_z
    else:
        return

    scale = 2
    pos2 = cube_positions * scale              
    min2 = pos2.min(axis=0)
    max2 = pos2.max(axis=0)

    center2 = (min2 + max2) // 2               

    relative2 = pos2 - center2                 
    for _ in range(k % 4):
        relative2 = (relative2 @ R.T)          
    pos2_rot = relative2 + center2

    return (pos2_rot // scale).astype(int)

#cube translate adding what's insiede the textboxes
def update_position(ax, event=None):
    global center, global_vertices_list
    try:
        tx = float(text_box_x.text)
        ty = float(text_box_y.text)
        tz = float(text_box_z.text)
        direction = np.array([tx, ty, tz], dtype=float)
        center = translate_center(center, direction)
        global_vertices_list = get_vertices_from_positions(cube_positions, center) #passes vector with translation info
        update_cubes(ax, global_vertices_list, colors)
    except ValueError:
        pass  

def rotate(event, axis, ax, colors):
    global cube_positions, center, global_vertices_list
    cube_positions = rotate_positions(cube_positions, axis, k=1)
    global_vertices_list = get_vertices_from_positions(cube_positions, center) # save vertices globally after rot
    update_cubes(ax, global_vertices_list, colors)

def validate_positions(ax):
    current_vertices =get_vertices_from_positions(cube_positions, center)
    invalid_found = False
    for i, vertices in enumerate(current_vertices):
        if np.any(vertices[:, 2] < 0):
            invalid_found = True
            break

    if invalid_found:
        print("not ok")
    else:
        print("ok")


def main():
    global global_vertices_list, center, cube_positions, colors, text_box_x, text_box_y, text_box_z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #little cubelets
    cube_positions = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)], dtype=int)
    center = np.array([0.0, 0.0, 0.0], dtype=float)

    colors = ['grey', 'blue', 'orange', 'green']

    global_vertices_list = get_vertices_from_positions(cube_positions, center)

    update_cubes(ax, global_vertices_list, colors)

    # translation buttons
    ax_btn_px = plt.axes([0.45, 0.01, 0.06, 0.075])
    btn_px = Button(ax_btn_px, '+X')
    btn_px.on_clicked(lambda event: translate(ax, np.array([1, 0, 0])))

    ax_btn_mx = plt.axes([0.52, 0.01, 0.06, 0.075])
    btn_mx = Button(ax_btn_mx, '-X')
    btn_mx.on_clicked(lambda event: translate(ax, np.array([-1, 0, 0])))

    ax_btn_py = plt.axes([0.59, 0.01, 0.06, 0.075])
    btn_py = Button(ax_btn_py, '+Y')
    btn_py.on_clicked(lambda event: translate(ax, np.array([0, 1, 0])))

    ax_btn_my = plt.axes([0.66, 0.01, 0.06, 0.075])
    btn_my = Button(ax_btn_my, '-Y')
    btn_my.on_clicked(lambda event: translate(ax, np.array([0, -1, 0])))

    ax_btn_pz = plt.axes([0.73, 0.01, 0.06, 0.075])
    btn_pz = Button(ax_btn_pz, '+Z')
    btn_pz.on_clicked(lambda event: translate(ax, np.array([0, 0, 1])))

    ax_btn_mz = plt.axes([0.80, 0.01, 0.06, 0.075])
    btn_mz = Button(ax_btn_mz, '-Z')
    btn_mz.on_clicked(lambda event: translate(ax, np.array([0, 0, -1])))

    #buttons for rotation
    ax_rot_x_90 = plt.axes([0.05, 0.01, 0.1, 0.075])
    btn_rot_x_90 = Button(ax_rot_x_90, 'Rotate X 90')

    ax_rot_y_90 = plt.axes([0.18, 0.01, 0.1, 0.075])
    btn_rot_y_90 = Button(ax_rot_y_90, 'Rotate Y 90')

    ax_rot_z_90 = plt.axes([0.31, 0.01, 0.1, 0.075])
    btn_rot_z_90 = Button(ax_rot_z_90, 'Rotate Z 90')

    ax_val_cube = plt.axes([0.88, 0.01, 0.1, 0.075])
    btn_val_cube = Button(ax_val_cube, "Check rot/pos")

    btn_rot_x_90.on_clicked(lambda event: rotate(event, 'x', ax, colors))
    btn_rot_y_90.on_clicked(lambda event: rotate(event, 'y', ax, colors))
    btn_rot_z_90.on_clicked(lambda event: rotate(event, 'z', ax, colors))
    btn_val_cube.on_clicked(lambda event: validate_positions(ax))


    plt.show()

if __name__ == "__main__":
    main()
