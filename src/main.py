from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from src.population import get_population
from utils import *

backpack = []
population_history = []
results_table = []
optimum_value = None

#=============================================================DEFAULT SETTINGS========================================================================

# Wstaw path dla danych i optimum
file_path = Path(fr"C:\Users\Seweryn\OneDrive\Desktop\Nowy folder (2)\AlgorytmyGenetyczne\dane AG\large_scale\knapPI_1_100_1000_1")
file_optimum_path = Path(fr"C:\Users\Seweryn\OneDrive\Desktop\Nowy folder (2)\AlgorytmyGenetyczne\dane AG\large_scale-optimum\knapPI_1_100_1000_1")

# Wybierz rodzaj testu
mode = "test_3"
    # "test_1" - Basic                          - jeden wykres
    # "test_2" - Mutacje 0.006 -> 0.01          - podajesz górną granicę mutation_rate, (iteruje od dołu 5 razy co 0.001)
    # "test_3" - Krzyżowanie 0.06 -> 1          - tu crossover_rate nie ustawiaj więcej jak 0.5 (iteruje 6 razy co 0.1 do wartości 1)
    # "test_4" - Ruletka Ranking                - selection_type nie jest uwzględniana
    # "test_5" - Krzyżowanie One- TwoPoint      - crossover_type nie jest uwzględniane
    # "test_6" - Ruletka Ranking Turniej        - selection_type nie jest uwzględniana

# Ustaw dowolnie iteracje i populacje, ew mutation rate lub crossover rate
iteration_count = 200
population_size = 50
mutation_rate = 0.01
crossover_type ="one_point"     # "one_point" "two_point"
crossover_rate = 0.5
selection_type = "roulette"     # "roulette", "ranking", "tournament"

#=====================================================================================================================================================

crossover_methods = {
    "one_point": one_point_crossover,
    "two_point": two_point_crossover,
}

selection_methods = {
    "tournament": tournament_selection,
    "roulette": roulette_selection,
    "ranking": ranking_selection,
}


def read_data(backpack):
    global optimum_value
    with open(file_path, 'r') as file:
        while True:
            line = file.readline().strip()
            if not line:
                break
            data = list(map(int, line.split()))
            backpack.append(data)

    with open(file_optimum_path, "r") as f:
        line2 = f.read().strip()
        optimum_value = float(line2)
        if optimum_value.is_integer():
            optimum_value = int(optimum_value)


def solve_knapsack(m_rate, c_rate, c_type, s_type):
    # funkcja przyjmuje wartości mutacji, krzyżowania, typ krzyżowania i typ selekcji
    # zwraca wygenerowaną krotkę z wygenerowaną listą "result" i parametrami obliczeń "params" do tabeli results_table

    crossover_function = crossover_methods[c_type]
    selection_function = selection_methods[s_type]
    read_data(backpack)
    best_in_given_iteration = []
    population = get_population(population_size, backpack[0][0], backpack)
    for _ in range(iteration_count):
        adaptive_with_values = get_adaptive_with_values(population, backpack)
        # save the best sample from adaptive with values before mutating etc
        population_history.append(adaptive_with_values)
        best = max(adaptive_with_values, key=lambda x: x[1])
        best_in_given_iteration.append(best)
        best_ten_creatures = sorted(adaptive_with_values, key=lambda x: x[1], reverse=True)[:10]
        new_population = []
        for b in best_ten_creatures:
            new_population.append(b[0])
        for i in range(0, int((population_size - 10) / 2)):
            # select 2 parents
            parent_one, parent_two = selection_function(adaptive_with_values)
            # crossover
            child_one, child_two = crossover_function(parent_one, parent_two, c_rate)
            # mutation
            child_one = mutate(m_rate, child_one)
            child_two = mutate(m_rate, child_two)
            # saving to new population
            new_population.append(child_one)
            new_population.append(child_two)
        # replacing population
        population = new_population
    # now time to format & save the outputs
    best_in_given_iteration_output = open("outputs/best_in_given_iteration.txt", "w")
    best_in_given_iteration_output.write(f"Iteration no. | highest value | weight | node\n")
    best_limited_output = open("outputs/best_limited_output.txt", "w")
    best_limited_output.write(f"Iteration no. | highest value\n")

    for i, best in enumerate(best_in_given_iteration):
        weight = 0
        node = best[0]
        for j in range(0, len(node)):
            if node[j] > 0:
                weight += backpack[j + 1][1]

        best_in_given_iteration_output.write(
            f"{i + 1} | {best_in_given_iteration[i][1]} | {weight} | {best_in_given_iteration[i][0]}\n")
        # print(f"{i+1} | {best_in_given_iteration[i][1]} | {weight} | {best_in_given_iteration[i][0]}\n")
        if i == 0:
            best_limited_output.write(f"{i + 1} | {best_in_given_iteration[i][1]}\n")
        else:
            if i >= 1 and (best_in_given_iteration[i - 1][1] != best_in_given_iteration[i][1]):
                best_limited_output.write(f"{i + 1} | {best_in_given_iteration[i][1]}\n")

    result = [x[1] for i, x in enumerate(best_in_given_iteration)]

    # parametry zwracane razem z wynikami do tablicy results_table
    params = {
        "mutation_rate": m_rate,
        "crossover_rate": c_rate,
        "crossover_type": c_type,
        "selection_type": s_type
    }

    return (result, params)


def draw_plot():
    # Funkcja rysująca wykres
    # Ustawienia początkowe
    iterations = list(range(1, iteration_count + 1))    # lista iteracji dla osi X
    plt.figure(figsize=(24, 12))                        # rozmiar okna
    font_size = 18                                      # większa czcionka dla tytułów
    second_font_size = 12                               # mniejsza czcionka dla ticków i napisów dodatkowych

    # Rysowanie linii / dane zależne od trybu
    legend_title = None  # inicjalizacja zmiennej legendy

    match mode:
        case "test_1":  # podstawowy pojedynczy wykres problemu
            plt.plot(iterations, results_table[0][0])
            plt.title("KNAPSACK RESULTS", fontsize=font_size)

        case "test_2":  # porównanie wartości mutacji
            for i in range(5):
                plt.plot(iterations, results_table[i][0], label=str(results_table[i][1]["mutation_rate"]))
            plt.title("COMPARISON OF MUTATION RATES", fontsize=font_size)
            legend_title = "Mutation rate"

        case "test_3":  # porównanie wartości krzyżowania
            for i in range(6):
                plt.plot(iterations, results_table[i][0], label=str(results_table[i][1]["crossover_rate"]))
            plt.title("COMPARISON OF CROSSOVER RATES", fontsize=font_size)
            legend_title = "Crossover rate"

        case "test_4":  # porównanie selekcji ruletki i rankingu
            plt.plot(iterations, results_table[0][0], label=results_table[0][1]["selection_type"])
            plt.plot(iterations, results_table[1][0], label=results_table[1][1]["selection_type"])
            plt.title("COMPARISON OF SELECTION TYPES", fontsize=font_size)
            legend_title = "Selection type"

        case "test_5":  # porównanie krzyżowania jedno- i dwupunktowego
            plt.plot(iterations, results_table[0][0], label=results_table[0][1]["crossover_type"])
            plt.plot(iterations, results_table[1][0], label=results_table[1][1]["crossover_type"])
            plt.title("COMPARISON OF CROSSOVER TYPES", fontsize=font_size)
            legend_title = "Crossover type"

        case "test_6":  # porównanie selekcji ruletki, rankingu, turnieju
            plt.plot(iterations, results_table[0][0], label=results_table[0][1]["selection_type"])
            plt.plot(iterations, results_table[1][0], label=results_table[1][1]["selection_type"])
            plt.plot(iterations, results_table[2][0], label=results_table[2][1]["selection_type"])
            plt.title("COMPARISON OF SELECTION TYPES", fontsize=font_size)
            legend_title = "Selection type"


    # Dodatki po narysowaniu linii
    # Linia optimum i napis nad nią
    plt.axhline(y=optimum_value, color='green', linestyle='-')
    plt.text(
        x=len(iterations)/2,
        y=optimum_value,
        s=f'Optimum = {optimum_value}',
        color='green',
        va='center',
        ha='center',
        backgroundcolor='white',
        fontsize=second_font_size
    )

    # Tytuły osi
    plt.xlabel("Iteration", fontsize=font_size)
    plt.ylabel("Value", fontsize=font_size)

    # Rozmiar wartości osi (ticków)
    plt.tick_params(axis='x', labelsize=second_font_size)
    plt.tick_params(axis='y', labelsize=second_font_size)

    # Wymuszenie osi X na wartości całkowite
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Legenda (tylko jeśli jest potrzeba)
    handles, labels = plt.gca().get_legend_handles_labels()
    if legend_title is not None:
        plt.legend(
            handles[::-1],
            labels[::-1],
            loc='best',
            title=legend_title,
            fontsize=second_font_size,
            title_fontsize=second_font_size
        )


    # Wyświetlenie wykresu
    plt.show()
    return


def main():
    """
    0. select type of comparing
    1. process args etc
    2. get the start population
    3. start iteration
    4. check if the sum of weight does not exceed
    5. select the creatures
    6. genetic operators
    7. new population created
    done

    in the meantime save the data to make a chart
    """
    global results_table

    # W results_table zachowuję historię wyników dla poszczególnych zmian w wartościach mutacji krzyżowania i selekcji

    match mode:
        case "test_1":  # podstawowy pojedyńczy wykres problemu
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, selection_type))
        case "test_2":  # porównanie wartości mutacji
            for i in range(5):
                results_table.append(
                    solve_knapsack(round(mutation_rate - (0.004 - 0.001 * i), 3), crossover_rate, crossover_type,selection_type))
        case "test_3":  # porównanie wartości krzyżowania
            for i in range(6):
                results_table.append(solve_knapsack(mutation_rate, crossover_rate + (0.1 * i), crossover_type, selection_type))
        case "test_4":  # porównanie selekcji ruletki i rankingu
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, "roulette"))
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, "ranking"))
            draw_plot()
        case "test_5":  # porównanie krzyżowania jedno- i dwupunktowego
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, "one_point", selection_type))
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, "two_point", selection_type))
        case "test_6":  # porównanie selekcji ruletki, rankingu, turnieju
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, "roulette"))
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, "ranking"))
            results_table.append(solve_knapsack(mutation_rate, crossover_rate, crossover_type, "tournament"))

    draw_plot()

if __name__ == '__main__':
    main()
