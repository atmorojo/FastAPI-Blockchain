import random


data_suhu = [
    [29.8],
    [28.9],
    [32.1],
    [33.7],  # Noisy reading
    [29.9]
]


def hitung_kebugaran(gagak):
    return max(gagak)  # Sesuaikan dengan masalah yang ingin diselesaikan


def gerak_gagak(gagak, memori_gagak, kemungkinan):
    if random.random() < kemungkinan:
        posisi_baru = [random.uniform(0, 1) for _ in gagak]
    else:
        posisi_baru = [
            g + random.random() * (m - g) for g, m in zip(gagak, memori_gagak)
        ]
    return posisi_baru


def csa(iterasi, kemungkinan):
    gagak = data_suhu[:]
    memori = gagak[:]
    jumlah_gagak = len(gagak)

    for _ in range(iterasi):
        for i in range(jumlah_gagak):
            gagak[i] = gerak_gagak(
                gagak[i], memori[random.randint(0, jumlah_gagak - 1)], kemungkinan
            )
            if hitung_kebugaran(gagak[i]) > hitung_kebugaran(memori[i]):
                memori[i] = gagak[i]

    hasil_terbaik = max(memori, key=hitung_kebugaran)
    return hasil_terbaik


print(csa(100, 0.2))
print(max(data_suhu))
