import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.widgets import Button, TextBox

# Definisce i vertici di un cubetto unitario
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

# Definisce le facce di un cubetto utilizzando i vertici
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

# Funzione per disegnare i cubetti
def draw_cubes(ax, vertices_list, colors):
    for vertices, color in zip(vertices_list, colors):
        faces = create_faces(vertices)
        ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.75))

# Matrice di rotazione per l'asse X
def rotation_matrix_x(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

# Matrice di rotazione per l'asse Y
def rotation_matrix_y(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

# Matrice di rotazione per l'asse Z
def rotation_matrix_z(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# Funzione per aggiornare la visualizzazione del cubo
def update_cubes(ax, vertices_list, colors):
    ax.cla()
    draw_cubes(ax, vertices_list, colors)
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    ax.set_zlim([0, 5])
    plt.draw()

# Funzione per gestire il clic del bottone di rotazione
def rotate(event, axis, angle, ax, colors):
    global global_vertices_list
    if axis == 'x':
        R = rotation_matrix_x(angle)
    elif axis == 'y':
        R = rotation_matrix_y(angle)
    elif axis == 'z':
        R = rotation_matrix_z(angle)
    else:
        return
    
    center = np.array([1, 1, 1]) + np.array([float(text_box_x.text), float(text_box_y.text), float(text_box_z.text)])
    global_vertices_list = [np.dot(vertices - center, R) + center for vertices in global_vertices_list]
    update_cubes(ax, global_vertices_list, colors)

# Funzione per aggiornare la posizione del cubo
def update_position(ax, event=None):
    global global_vertices_list, offsets
    try:
        center = np.array([float(text_box_x.text), float(text_box_y.text), float(text_box_z.text)])
        global_vertices_list = [create_unit_cube(offset + center) for offset in offsets]
        update_cubes(ax, global_vertices_list, colors)
    except ValueError:
        pass  # Ignora se il testo non è un numero valido

# Funzione principale
def main():
    global global_vertices_list, offsets, colors, text_box_x, text_box_y, text_box_z
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Crea i cubetti con offset specifici
    offsets = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 1)]
    center = np.array([0, 0, 0])
    global_vertices_list = [create_unit_cube(offset + center) for offset in offsets]

    # Colori distinti per ogni cubetto
    colors = ['grey', 'grey', 'grey', 'grey']
    draw_cubes(ax, global_vertices_list, colors)

    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    ax.set_zlim([0, 5])

    # Caselle di testo per il posizionamento
    ax_box_x = plt.axes([0.2, 0.15, 0.1, 0.05])
    text_box_x = TextBox(ax_box_x, 'X', initial="0")

    ax_box_y = plt.axes([0.35, 0.15, 0.1, 0.05])
    text_box_y = TextBox(ax_box_y, 'Y', initial="0")

    ax_box_z = plt.axes([0.5, 0.15, 0.1, 0.05])
    text_box_z = TextBox(ax_box_z, 'Z', initial="0")

    text_box_x.on_text_change(lambda val: update_position(ax))
    text_box_y.on_text_change(lambda val: update_position(ax))
    text_box_z.on_text_change(lambda val: update_position(ax))

    # Aggiunge i bottoni di rotazione per l'asse X
    ax_rot_x_90 = plt.axes([0.1, 0.01, 0.1, 0.075])
    btn_rot_x_90 = Button(ax_rot_x_90, 'Rotate X 90')

    # Aggiunge i bottoni di rotazione per l'asse Y
    ax_rot_y_90 = plt.axes([0.43, 0.01, 0.1, 0.075])
    btn_rot_y_90 = Button(ax_rot_y_90, 'Rotate Y 90')

    # Aggiunge i bottoni di rotazione per l'asse Z
    ax_rot_z_90 = plt.axes([0.76, 0.01, 0.1, 0.075])
    btn_rot_z_90 = Button(ax_rot_z_90, 'Rotate Z 90')

    btn_rot_x_90.on_clicked(lambda event: rotate(event, 'x', np.pi/2, ax, colors))
    btn_rot_y_90.on_clicked(lambda event: rotate(event, 'y', np.pi/2, ax, colors))
    btn_rot_z_90.on_clicked(lambda event: rotate(event, 'z', np.pi/2, ax, colors))

    plt.show()

if __name__ == "__main__":
    main()
