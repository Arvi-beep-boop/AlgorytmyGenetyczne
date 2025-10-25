
VALUE_IDX = 0
WEIGHT_IDX = 1

backpack = []

def read_data(filepath, backpack):
    # EXPECTED FILE STRUCTURE:
    # Wielkosc_problemu pojemnosc
    # wartosc_przedmiotu_1 waga_przedmiotu_1
    # ....
    # wartosc_przedmiotu_n waga_przedmiotu_n
    with open(filepath, 'r') as file:
        while True:
            line = file.readline().strip()
            if not line:
                break
            data = list(map(int, line.split()))
            backpack.append(data)

read_data('../dane AG/low-dimensional/f1_l-d_kp_10_269', backpack)

print(backpack)