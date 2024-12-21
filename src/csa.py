import numpy as np


# Fungsi objektif untuk menemukan nilai minimum
def min_function(position, x_values):
    # Posisi diindeks dari array x_values
    return x_values[int(position)]


def max_function(position, x_values):
    # Posisi diindeks dari array x_values
    return -x_values[int(position)]


# Inisialisasi posisi burung gagak dalam ruang satu dimensi (array x_values)
def initialize_population(num_crows, x_values):
    return np.random.randint(
        0, len(x_values), size=num_crows
    )  # Posisi adalah indeks dalam array


# Fungsi pembaruan posisi gagak dalam ruang satu dimensi
def update_crow_position(
    crow_position, global_best_position, num_positions, alpha=0.5, beta=1.5
):
    random_value = np.random.uniform(-1, 1)
    new_position = (
        crow_position
        + alpha * (global_best_position - crow_position)
        + beta * random_value
    )
    # Pastikan posisi berada dalam batas array x_values
    new_position = max(0, min(int(new_position), num_positions - 1))
    return new_position


# Crow Search Algorithm (CSA)
def crow_search_algorithm(
    objective_function, x_values, num_crows, num_iterations
):
    num_positions = len(x_values)
    # Inisialisasi posisi gagak secara acak (indeks dari array x_values)
    crows_positions = initialize_population(num_crows, x_values)

    # Cari posisi global terbaik dari populasi awal
    global_best_position = crows_positions[
        np.argmin(
            [objective_function(pos, x_values) for pos in crows_positions]
        )
    ]

    # Jalankan iterasi
    for _ in range(num_iterations):
        for i in range(num_crows):
            # Pembaruan posisi setiap gagak
            new_position = update_crow_position(
                crows_positions[i], global_best_position, num_positions
            )
            # Jika posisi baru lebih baik, perbarui posisi gagak
            if objective_function(
                new_position, x_values
            ) < objective_function(crows_positions[i], x_values):
                crows_positions[i] = new_position

            # Perbarui posisi global terbaik jika ditemukan solusi yang lebih baik
            if objective_function(
                crows_positions[i], x_values
            ) < objective_function(global_best_position, x_values):
                global_best_position = crows_positions[i]

    # Mengembalikan solusi global terbaik (indeks)
    return global_best_position


# Parameter CSA
num_crows = 10  # Jumlah gagak
num_iterations = 100  # Jumlah iterasi

# Jalankan algoritma Crow Search Algorithm
def max_value(values):
    x_values = np.array(values)
    return x_values[crow_search_algorithm(
        max_function, x_values, num_crows, num_iterations
    )]


def min_value(values):
    x_values = np.array(values)
    return x_values[crow_search_algorithm(
        min_function, x_values, num_crows, num_iterations
    )]

""" Usage example
print("Posisi terbaik ditemukan pada indeks:", best_position)
print("Nilai minimum yang ditemukan:", x_values[best_position])
"""
