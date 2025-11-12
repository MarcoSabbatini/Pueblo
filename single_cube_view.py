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
def update_cubes(ax):
    ax.cla()
    for cube in cubes:
        cube.draw(ax)
    if current_cube:
        current_cube.draw(ax)
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
        return cube_positions

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


cubes = []
current_cube = None

class Cube:
    def __init__(self, cube_positions, center, colors):
        self.positions = cube_positions
        self.center = center
        self.colors = colors
        self.vertices_list = get_vertices_from_positions(cube_positions, center)
        
    def draw(self, ax):
        draw_cubes(ax, self.vertices_list, self.colors)
        
    def translate_center(self, direction):
        self.center += direction
        self.vertices_list = get_vertices_from_positions(self.positions, self.center)
        
    def rotate(self, axis, k=1):
        self.positions = rotate_positions(self.positions, axis, k)
        self.vertices_list = get_vertices_from_positions(self.positions, self.center)

def rotate(event, axis, ax, colors):
    global cube_positions, center, global_vertices_list
    cube_positions = rotate_positions(cube_positions, axis, k=1)
    global_vertices_list = get_vertices_from_positions(cube_positions, center) # save vertices globally after rot
    update_cubes(ax, global_vertices_list, colors)

def validate_positions(ax, silent=False):
    global current_cube, cubes
    
    if current_cube is None:
        if not silent:
            print("no cube to validate")
        return False
    
    current_vertices = get_vertices_from_positions(current_cube.positions, current_cube.center)
    
    for vertices in current_vertices:
        if np.any(vertices[:, 2] < 0):
            if not silent:
                print('under ground, not ok')
            return False
    
    for fixed_cube in cubes:
        for pos_fixed in fixed_cube.positions + fixed_cube.center:
            for pos_current in current_cube.positions + current_cube.center:
                if np.allclose(pos_fixed, pos_current):
                    if not silent:
                        print('overlaps with other cubes, not ok')
                    return False
                
    support_count = 0
    for pos_current in current_cube.positions + current_cube.center:
        below = pos_current.copy()
        below[2] -= 1 # look right below the cubelet
        # check if below is ground or another cubelet
        if below[2] < 0:
            support_count += 1
        else:
            for fixed_cube in cubes:
                for pos_fixed in fixed_cube.positions + fixed_cube.center:
                    if np.allclose(pos_fixed, below):
                        support_count += 1
                        break # found something
        if support_count >= 2:
            break # ok, can be fixed
    
    if support_count < 2:
        if not silent:
            print(f"not enough support ({support_count} cubelets touching), not ok")
        return False
    
    if not silent:
        print('ok')
    return True

def add_new_cube(ax):
    global current_cube
    if current_cube is not None:
        print("not permanently added, restart rot/trasl of same new cube")
    else:
        print('new cube')
    offset = np.array([0.0, 0.0, 0.0], dtype=float)
    if cubes:
        # if there are already cubes, put the new beside it
        offset = cubes[-1].center + np.array([2.0, 0.0, 0.0])
    cube_positions = np.array([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)], dtype=int)
    cube_colors = ['red', 'yellow', 'cyan', 'magenta']
    current_cube = Cube(cube_positions, offset, cube_colors)
    update_cubes(ax)

def fix_current_cube(ax):
    global current_cube
    if current_cube:
        if not validate_positions(ax, silent=True):
            print("not fixed because not valid")
            return
        cubes.append(current_cube)
        print("cube fixed:", current_cube.center)
        current_cube = None
        update_cubes(ax)
    else:
        print("noc ube to fix")

def main():
    global global_vertices_list, cube_positions, current_cube
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # translation buttons
    ax_btn_px = plt.axes([0.45, 0.01, 0.06, 0.075])
    btn_px = Button(ax_btn_px, '+X')
    btn_px.on_clicked(lambda event: (current_cube.translate_center(np.array([1,0,0])), update_cubes(ax)) if current_cube else None)

    ax_btn_mx = plt.axes([0.52, 0.01, 0.06, 0.075])
    btn_mx = Button(ax_btn_mx, '-X')
    btn_mx.on_clicked(lambda event: (current_cube.translate_center(np.array([-1,0,0])), update_cubes(ax)) if current_cube else None)

    ax_btn_py = plt.axes([0.59, 0.01, 0.06, 0.075])
    btn_py = Button(ax_btn_py, '+Y')
    btn_py.on_clicked(lambda event: (current_cube.translate_center(np.array([0,1,0])), update_cubes(ax)) if current_cube else None)

    ax_btn_my = plt.axes([0.66, 0.01, 0.06, 0.075])
    btn_my = Button(ax_btn_my, '-Y')
    btn_my.on_clicked(lambda event: (current_cube.translate_center(np.array([0,-1,0])), update_cubes(ax)) if current_cube else None)

    ax_btn_pz = plt.axes([0.73, 0.01, 0.06, 0.075])
    btn_pz = Button(ax_btn_pz, '+Z')
    btn_pz.on_clicked(lambda event: (current_cube.translate_center(np.array([0,0,1])), update_cubes(ax)) if current_cube else None)

    ax_btn_mz = plt.axes([0.80, 0.01, 0.06, 0.075])
    btn_mz = Button(ax_btn_mz, '-Z')
    btn_mz.on_clicked(lambda event: (current_cube.translate_center(np.array([0,0,-1])), update_cubes(ax)) if current_cube else None)

    #buttons for rotation
    ax_rot_x_90 = plt.axes([0.05, 0.01, 0.1, 0.075])
    btn_rot_x_90 = Button(ax_rot_x_90, 'Rotate X 90')

    ax_rot_y_90 = plt.axes([0.18, 0.01, 0.1, 0.075])
    btn_rot_y_90 = Button(ax_rot_y_90, 'Rotate Y 90')

    ax_rot_z_90 = plt.axes([0.31, 0.01, 0.1, 0.075])
    btn_rot_z_90 = Button(ax_rot_z_90, 'Rotate Z 90')

    ax_val_cube = plt.axes([0.88, 0.01, 0.1, 0.075])
    btn_val_cube = Button(ax_val_cube, "Check rot/pos")

    ax_btn_new_cube = plt.axes([0.88, 0.17, 0.1, 0.075])
    btn_new_cube = Button(ax_btn_new_cube, "New Cube")
    
    ax_btn_fix_cube = plt.axes([0.88, 0.25, 0.1, 0.075])
    btn_fix_cube = Button(ax_btn_fix_cube, "Fix Cube")
    
    btn_fix_cube.on_clicked(lambda event: fix_current_cube(ax))
    btn_new_cube.on_clicked(lambda event: add_new_cube(ax))
    btn_rot_x_90.on_clicked(lambda event: (current_cube.rotate('x'), update_cubes(ax)) if current_cube else None)
    btn_rot_y_90.on_clicked(lambda event: (current_cube.rotate('y'), update_cubes(ax)) if current_cube else None)
    btn_rot_z_90.on_clicked(lambda event: (current_cube.rotate('z'), update_cubes(ax)) if current_cube else None)
    btn_val_cube.on_clicked(lambda event: validate_positions(ax))


    plt.show()

if __name__ == "__main__":
    main()
