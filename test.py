import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def draw_little_cubes(ax, position, color='cyan'):
    x, y, z = position
    vertices = [
        [[x, y, z], [x+1, y, z], [x+1, y+1, z], [x, y+1, z]],
        [[x, y, z+1], [x+1, y, z+1], [x+1, y+1, z+1], [x, y+1, z+1]],
        [[x, y, z], [x, y+1, z], [x, y+1, z+1], [x, y, z+1]],
        [[x+1, y, z], [x+1, y+1, z], [x+1, y+1, z+1], [x+1, y, z+1]],
        [[x, y, z], [x+1, y, z], [x+1, y, z+1], [x, y, z+1]],
        [[x, y+1, z], [x+1, y+1, z], [x+1, y+1, z+1], [x, y+1, z+1]]
    ]
    faces = Poly3DCollection(vertices, alpha=0.25, edgecolor='k', facecolor=color)
    ax.add_collection3d(faces)

def rotate_z_90(tetracube):
    return [
        (tetracube[0][0], tetracube[0][1] + 1, tetracube[0][2]),  # (x, y+1, z)
        (tetracube[1][0] - 1, tetracube[1][1], tetracube[1][2]),  # (x-1, y, z)
        (tetracube[2][0] + 1, tetracube[2][1], tetracube[2][2]),  # (x+1, y, z)
        (tetracube[3][0] + 1, tetracube[3][1], tetracube[3][2])   # (x+1, y, z)
    ]

def rotate_z_180(tetracube):
    return [
        (tetracube[0][0] + 1, tetracube[0][1] + 1, tetracube[0][2]),  # (x+1, y+1, z)
        (tetracube[1][0] - 1, tetracube[1][1] + 1, tetracube[1][2]),  # (x-1, y+1, z)
        (tetracube[2][0] + 1, tetracube[2][1] - 1, tetracube[2][2]),  # (x+1, y-1, z)
        (tetracube[3][0] + 1, tetracube[3][1] - 1, tetracube[3][2])   # (x+1, y-1, z)
    ]

def rotate_z_270(tetracube):
    return [
        (tetracube[0][0] + 1, tetracube[0][1], tetracube[0][2]),  # (x+1, y, z)
        (tetracube[1][0], tetracube[1][1] + 1, tetracube[1][2]),  # (x, y+1, z)
        (tetracube[2][0], tetracube[2][1] + 1, tetracube[2][2]),  # (x, y+1, z)
        (tetracube[3][0], tetracube[3][1] + 1, tetracube[3][2])   # (x, y+1, z)
    ]

def rotate_y_90(tetracube):
    return [
        (tetracube[0][0], tetracube[0][1], tetracube[0][2] + 1),  # (x, y, z+1)
        (tetracube[1][0] - 1, tetracube[1][1], tetracube[1][2]),  # (x-1, y, z)
        (tetracube[2][0], tetracube[2][1], tetracube[2][2] + 1),  # (x, y, z+1)
        (tetracube[3][0] + 1, tetracube[3][1], tetracube[3][2])   # (x+1, y, z)
    ]

def rotate_y_180(tetracube):
    return [
        (tetracube[0][0] + 1, tetracube[0][1], tetracube[0][2] + 1),  # (x+1, y, z+1)
        (tetracube[1][0] - 1, tetracube[1][1], tetracube[1][2] + 1),  # (x-1, y, z+1)
        (tetracube[2][0] + 1, tetracube[2][1], tetracube[2][2] + 1),  # (x+1, y, z+1)
        (tetracube[3][0] + 1, tetracube[3][1], tetracube[3][2] - 1)   # (x+1, y, z-1)
    ]

def rotate_y_270(tetracube):
    return [
        (tetracube[0][0] + 1, tetracube[0][1], tetracube[0][2]),  # (x+1, y, z)
        (tetracube[1][0], tetracube[1][1], tetracube[1][2] + 1),  # (x, y, z+1)
        (tetracube[2][0] + 1, tetracube[2][1], tetracube[2][2]),  # (x+1, y, z)
        (tetracube[3][0], tetracube[3][1], tetracube[3][2] - 1)   # (x, y, z-1)
    ]

def rotate_x_90(tetracube):
    return [
        (tetracube[0][0], tetracube[0][1], tetracube[0][2] + 1),  # (x, y, z+1)
        (tetracube[1][0], tetracube[1][1], tetracube[1][2] + 1),  # (x, y, z+1)
        (tetracube[2][0], tetracube[2][1] - 1, tetracube[2][2]),  # (x, y-1, z)
        (tetracube[3][0], tetracube[3][1], tetracube[3][2] - 1)   # (x, y, z-1)
    ]

def rotate_x_180(tetracube):
    return [
        (tetracube[0][0], tetracube[0][1] + 1, tetracube[0][2] + 1),  # (x, y+1, z+1)
        (tetracube[1][0], tetracube[1][1] + 1, tetracube[1][2] + 1),  # (x, y+1, z+1)
        (tetracube[2][0], tetracube[2][1] - 1, tetracube[2][2] + 1),  # (x, y-1, z+1)
        (tetracube[3][0], tetracube[3][1] - 1, tetracube[3][2] - 1)   # (x, y-1, z-1)
    ]

def rotate_x_270(tetracube):
    return [
        (tetracube[0][0], tetracube[0][1] + 1, tetracube[0][2]),  # (x, y+1, z)
        (tetracube[1][0], tetracube[1][1] + 1, tetracube[1][2]),  # (x, y+1, z)
        (tetracube[2][0], tetracube[2][1], tetracube[2][2] + 1),  # (x, y, z+1)
        (tetracube[3][0], tetracube[3][1] - 1, tetracube[3][2])   # (x, y-1, z)
    ]

# Funzione per applicare la rotazione a un tetracubo
def rotate_tetracube(tetracube, axis, angle):
    if angle not in [90, 180, 270]:
        raise ValueError("Angle must be 90, 180, or 270 degrees")
    
    rotation_funcs = {
        'x': {90: rotate_x_90, 180: rotate_x_180, 270: rotate_x_270},
        'y': {90: rotate_y_90, 180: rotate_y_180, 270: rotate_y_270},
        'z': {90: rotate_z_90, 180: rotate_z_180, 270: rotate_z_270}
    }
    
    rotate_func = rotation_funcs[axis][angle]
    return rotate_func(tetracube)

# Function to apply translation to a tetracube
def translate_tetracube(tetracube, translation_vector):
    tx, ty, tz = translation_vector
    return [(x + tx, y + ty, z + tz) for x, y, z in tetracube]

def has_two_faces_touching_ground_or_other_tetracubes(tetracube, environment_tetracubes):
    environment_cubes_set = set(cube for tetracube in environment_tetracubes for cube in tetracube)
    count_touching_faces = 0

    for x, y, z in tetracube:
        faces_touching = 0
        
        # Check if the face down is touching the ground
        if z == 0:
            faces_touching += 1
        # Check if the face down is touching the top face of another cube in the environment
        elif (x, y, z - 1) in environment_cubes_set:
            faces_touching += 1
        
        if faces_touching > 0:
            count_touching_faces += 1
        
        if count_touching_faces >= 2:
            return True

    return False

def do_tetracubes_overlap(tetracube1, tetracube2):
    # Convertire le liste di cubi in set per consentire un confronto rapido
    set_tetracube1 = set(tetracube1)
    set_tetracube2 = set(tetracube2)
    
    # Intersecare i due set e verificare se esiste almeno un elemento comune
    overlap = set_tetracube1 & set_tetracube2
    
    return len(overlap) > 0

def insert_new_tetracube(existing_tetracubes):
    while True:
        try:
            # Input delle coordinate per il nuovo tetracubo
            print("Inserisci le coordinate per il nuovo tetracubo (formato: x,y,z)")
            input_str = input("Coordinate: ")
            x, y, z = map(int, input_str.split(','))

            rotate_option = input("Vuoi ruotare il tetracubo? (s/n): ").lower()
            if rotate_option == 's':
                axis = input("Scegli l'asse di rotazione (x, y, z): ").lower()
                angle = int(input("Scegli l'angolo di rotazione (90, 180, 270): "))
                new_tetracube = rotate_tetracube([(x, y, z), (x + 1, y, z), (x, y + 1, z), (x, y + 1, z + 1)], axis, angle)
            else:
                new_tetracube = [(x, y, z), (x + 1, y, z), (x, y + 1, z), (x, y + 1, z + 1)]
            
            # Verifica se il nuovo tetracubo si sovrappone con quelli già presenti
            overlap = False
            for tetracube in existing_tetracubes:
                if any(cube in tetracube for cube in new_tetracube):
                    overlap = True
                    print("Il nuovo tetracubo si sovrappone con un tetracubo già presente.")
                    break
            
            if overlap:
                continue  # Chiedi nuove coordinate se c'è sovrapposizione
            
            # Verifica la condizione has_two_faces_touching_ground_or_other_tetracubes
            if not has_two_faces_touching_ground_or_other_tetracubes(new_tetracube, existing_tetracubes):
                print("Il nuovo tetracubo non soddisfa la condizione richiesta.")
                continue  # Chiedi nuove coordinate se non soddisfa la condizione
            
            # Se tutto è ok, aggiungi il nuovo tetracubo alla lista e esci dalla funzione
            existing_tetracubes.append(new_tetracube)
            print("Nuovo tetracubo aggiunto correttamente!")
            return new_tetracube  # Restituisce il nuovo tetracubo aggiunto
        
        except ValueError:
            print("Input non valido. Assicurati di inserire le coordinate nel formato corretto.")

def plot_3d_grid(tetracubes, x_increment=1, z_increment=1):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'orange', 'purple']

    for index, tetracube in enumerate(tetracubes):
        color = colors[index % len(colors)]
        for cube in tetracube:
            draw_little_cubes(ax, cube, color)
            center_x = cube[0] + 0.5
            center_y = cube[1] + 0.5
            center_z = cube[2] + 0.5
            ax.text(center_x, center_y, center_z, f'{index}', color='black', fontsize=8, ha='center', va='center')
    
    # Impostare i tick per l'asse X
    x_ticks = np.arange(0, 15, x_increment)
    ax.set_xticks(x_ticks)
    
    # Impostare i tick per l'asse Z
    z_ticks = np.arange(0, 6, z_increment)
    ax.set_zticks(z_ticks)
    
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_zlim(0, 6)
    
    plt.show()

# Define the R-Screw tetracubes
tetracube_original = [(1, 1, 0), (2, 1, 0), (1, 2, 0), (1, 2, 1)]  # Original R-Screw example
tetracube1 =         [(1, 1, 0), (2, 1, 0), (1, 2, 0), (1, 2, 1)]  # Cubi a livello del suolo
tetracube2 = [(3, 0, 0), (4, 0, 0), (3, 1, 0), (3, 1, 1)]

# Create a list to store all tetracubes with their transformations
tetracubes = [
    #z axis rotation
    [(1, 1, 0), (2, 1, 0), (1, 2, 0), (1, 2, 1)], #original
    #[(x, y+1, z), (x-1, y, z), (x+1, y, z), (x+1, y, z)], #90 deegres
    #[(x+1, y+1, z), (x-1, y+1, z), (x+1, y-1, z), (x+1, y-1, z)], #180 degrees
    #[(x+1, y, z), (x, y+1, z), (x, y+1, z), (x, y+1, z)], #270 degrees

    #y axis rotation
    #[(1, 1, 0), (2, 1, 0), (1, 2, 0), (1, 2, 1)], #original
    #[(x, y, z+1), (x-1, y, z), (x, y, z+1), (x+1, y, z)] #90 degrees
    #[(x+1, y, z+1), (x-1, y, z+1), (x+1, y, z+1), (x+1, y, z-1)] #180 degrees
    #[(x+1, y, z), (x, y, z+1), (x+1, y, z), (x, y, z-1)] #270 degrees

    #y axis rotation
    #[(1, 1, 0), (2, 1, 0), (1, 2, 0), (1, 2, 1)], #original
    #[(x, y, z+1), (x, y, z+1), (x, y-1, z), (x, y, z-1)] #90 degrees
    #[(x, y+1, z+1), (x, y+1, z+1), (x, y-1, z+1), (x, y-1, z-1)] #180 degrees
    #[(x, y+1, z), (x, y+1, z), (x, y, z+1), (x, y-1, z)] #270 degrees
]

#plot_3d_grid(tetracubes, 1, 1)
#Loop to insert new tetracubes until the user decides to stop
#while True:
insert_new_tetracube(tetracubes)
plot_3d_grid(tetracubes, x_increment=1, z_increment=1)
    
#    continue_option = input("Vuoi inserire un altro tetracubo? (s/n): ").lower()
#    if continue_option != 's':
#        break
