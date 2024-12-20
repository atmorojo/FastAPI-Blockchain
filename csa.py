import numpy as np

# Fungsi objektif: Mencari nilai maksimum dan minimum dalam data
def objective_function(data):
    return np.max(data), np.min(data)

# Inisialisasi populasi gagak, diganti dengan 
# data blockchain yang sesuai dengan token tertentu seperti token untuk
# data sensor pengiriman produk per-alat transportasi
def initialize_population(num_crows, data_length):
    return np.random.uniform(0, 100, size=(num_crows, data_length))

# Fungsi pembaruan posisi gagak (dapat disesuaikan)
def update_crow_position(crow_position, global_best_position, alpha=0.5, beta=1.5):
    # Pembaruan posisi menggunakan aturan CSA
    new_position = crow_position + alpha * (crow_position - global_best_position) + beta * np.random.uniform(-1, 1)
    return new_position

# Crow Search Algorithm
def crow_search_algorithm(objective_function, data, num_crows, num_iterations):
    crows_positions = initialize_population(num_crows, len(data))
    global_best_position = crows_positions[np.argmax([objective_function(x) for x in crows_positions])]

    for iteration in range(num_iterations):
        for i in range(num_crows):
            # Evaluasi fungsi objektif
            current_fitness = objective_function(crows_positions[i])
            best_fitness = objective_function(global_best_position)

            # Pembaruan posisi
            crows_positions[i] = update_crow_position(crows_positions[i], global_best_position)

            # Perbarui posisi terbaik jika ditemukan yang lebih baik
            if objective_function(crows_positions[i])[0] > best_fitness[0]:
                global_best_position = crows_positions[i]

    return global_best_position

# Inisialisasi data acak
random_data = np.random.uniform(0, 100, 20)

# Set jumlah gagak dan iterasi
num_crows = 50
num_iterations = 100

# Jalankan Crow Search Algorithm
best_solution = crow_search_algorithm(objective_function, random_data, num_crows, num_iterations)

print("Data acak:", random_data)
maksimal,minimal = objective_function(random_data)
print("Nilai maksimum dalam data acak:"+str(maksimal))
print("Nilai minimum dalam data acak:"+str(minimal))
