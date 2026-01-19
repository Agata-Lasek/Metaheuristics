import random
import math
import csv
from Fitness import fitness
from Zachlanny import zachlanny

# operacje na permutacji

def _swap(sol): 
    zmieniona_perm = sol.copy()                  # kopiuje listę
    i = random.randrange(len(zmieniona_perm))    # losuje indeks i
    j = random.randrange(len(zmieniona_perm))    # losuje indeks j
    zmieniona_perm[i], zmieniona_perm[j] = zmieniona_perm[j], zmieniona_perm[i] # zamieniam wartości i i j miejscami
    return zmieniona_perm

def _invert(sol):
    zmieniona_perm = sol.copy()
    i = random.randrange(len(zmieniona_perm))   # losuje indeks i
    j = random.randrange(len(zmieniona_perm))   # losuje indeks j
    if i > j:                                   # upewniam się, że i <= j, żeby poprawnie wyciąć fragment listy od lewej do prawej, to są indeksy, nie nr miast
        i, j = j, i
    zmieniona_perm[i:j+1] = list(reversed(zmieniona_perm[i:j+1]))   # odwracam fragment między i a j włącznie
    return zmieniona_perm




def symulowane_wyzarzanie(dane, macierz, klienci, depot,
                          T0=100.0, Tmin=0.001, alpha=0.98,
                          iteracje=100, rodzaj_ruchu=0.7,
                          csv_path=None, seed=None):

    if seed is not None:        # jeśli chcę powtażać wyniki seed do ustawienia, na razie None
        random.seed(seed)

    # na start rozwiązanie zachłanne
    perm, koszt = zachlanny(dane, macierz, klienci, depot)
    najlepsza_perm = perm.copy()    # kopia najlepszej znalezionej permutacji
    najlepszy_koszt = koszt         # koszt najlepszej permutacji

    T = float(T0)                   # Temperatura początkowa

    # Struktury do zbierania danych
    temperature_cost_data = []      # lista krotek (T, best_cost_in_temp)
    generation_best_costs = []      # najlepszy koszt dla każdej temperatury

    # globalny przebieg cost vs iteracja
    iter_costs = []                 # zapis (numer_iteracji_globalnej, koszt)
    global_iter = 0                 # licznik iteracji całego procesu

    # Pętla chłodzenia / Algorytm działa tak długo, aż temperatura spadnie poniżej minimalnej
    while T > Tmin:
        gen_best_cost = najlepszy_koszt

        for it in range(iteracje):                  # Przy danej temperaturze wykonuje określoną liczbę prób
            # wybór ruchu
            if random.random() < rodzaj_ruchu:      # Wybór ruchu/ na start swap (70%) lub inversion (30%)
                kand = _swap(perm)
            else:
                kand = _invert(perm)

            koszt_nowy, _ = fitness(kand, macierz, dane["demands"], dane["capacity"], depot)    #  koszt nowej permutacji, liczony przez funkcję fitness
            delta = koszt_nowy - koszt              # różnica rozwiązań, czy lepsze, czy gorsze

            if delta < 0 or (T > 0 and random.random() < math.exp(-delta / T)): # Nowe rozwiązanie zostaje przyjęte zawsze jeśli jest lepsze, czasami jeśli jest gorsze, zależne od temperatury
                perm, koszt = kand, koszt_nowy

            if koszt < najlepszy_koszt:         # Aktualizacja najlepszego rozwiązania globalnie
                najlepszy_koszt = koszt
                najlepsza_perm = perm.copy()    # kopia, bo perm będzie modyfikowana w kolejnych iteracjach, bez kopii najlepsza_perm zmieniałaby się razem z nią i nie zachowałaby najlepszego znalezionego rozwiązania


            # zapis kosztu względem globalnej iteracji, na potem do csv
            iter_costs.append((global_iter, koszt))
            global_iter += 1

            if koszt < gen_best_cost:       # zapisuje najlepszy koszt znaleziony w obrębie jednej temperatury, żeby po zakończeniu tej temperatury wiedzieć, jaki był jej najlepszy wynik
                gen_best_cost = koszt

        temperature_cost_data.append((T, gen_best_cost))    # Po zakończeniu danej temperatury zapisuje statystyki
        generation_best_costs.append(gen_best_cost)

        T *= alpha          # Chłodzenie temperatury

    #  zapis przebiegu cost vs iteracja do CSV
    if csv_path:
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["iteracja", "cost"])
            for it_idx, c in iter_costs:
                writer.writerow([it_idx, c])

    return najlepsza_perm, najlepszy_koszt, temperature_cost_data, generation_best_costs