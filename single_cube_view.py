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

"""def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


#gets the avg of the whole cube
def get_global_center(vertices_list):
    all_points = np.vstack(vertices_list) # puts one on top of the other the rows, impiles one over each other, they have to be the same dim
    return np.mean(all_points, axis=0)
"""

#related to center
def get_vertices_from_positions(cube_positions, center):
    vertices_list = []
    for pos in cube_positions:
        offset = center + pos
        vertices_list.append(create_unit_cube(offset))
    return vertices_list

def translate_center(center, tx, ty, tz):
    return center + np.array([tx, ty, tz])

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

    # scala interna per gestire mezze unità: moltiplichiamo per 2
    scale = 2
    pos2 = cube_positions * scale              # ora sono interi (multipli di 2)
    min2 = pos2.min(axis=0)
    max2 = pos2.max(axis=0)

    # centro della bounding box in scala 2: (min2 + max2) / 2 -> sempre intero
    center2 = (min2 + max2) // 2               # intero preciso nello spazio scalato

    # trasliamo al centro, ruotiamo k volte, ritrasliamo
    relative2 = pos2 - center2                 # valori interi
    for _ in range(k % 4):
        # rotation in the doubled lattice: R maps integers->integers
        relative2 = (relative2 @ R.T)          # row-vector convention
    pos2_rot = relative2 + center2

    # torniamo alla scala originale dividendo per 2
    # pos2_rot deve essere multiplo di 2 se tutto è coerente -> divisione esatta
    return (pos2_rot // scale).astype(int)

#rotation function on click
"""def rotate(event, axis, angle, ax, colors):
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
"""

#cube translate adding what's insiede the textboxes
def update_position(ax, event=None):
    global center
    try:
        tx = float(text_box_x.text)
        ty = float(text_box_y.text)
        tz = float(text_box_z.text)
        #translation = np.array([tx, ty, tz])

        center = translate_center(center, tx, ty, tz)
        global_vertices_list = get_vertices_from_positions(cube_positions, center)
        update_cubes(ax, global_vertices_list, colors)
    except ValueError:
        pass  

def rotate(event, axis, ax, colors):
    global cube_positions, center
    cube_positions = rotate_positions(cube_positions, axis, k=1)
    vertices_list = get_vertices_from_positions(cube_positions, center)
    update_cubes(ax, vertices_list, colors)

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
    global global_vertices_list, center, cube_positions, colors, text_box_x, text_box_y, text_box_z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #little cubelets
    cube_positions = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)], dtype=int)
    center = np.array([0.0, 0.0, 0.0], dtype=float)

    colors = ['grey', 'blue', 'orange', 'green']

    global_vertices_list = get_vertices_from_positions(cube_positions, center)

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

    btn_rot_x_90.on_clicked(lambda event: rotate(event, 'x', ax, colors))
    btn_rot_y_90.on_clicked(lambda event: rotate(event, 'y', ax, colors))
    btn_rot_z_90.on_clicked(lambda event: rotate(event, 'z', ax, colors))
    btn_val_cube.on_clicked(lambda event: validate_positions(ax, cube_positions, center, colors))


    plt.show()

if __name__ == "__main__":
    main()
