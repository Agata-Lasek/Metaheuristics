from dane import czytanie_danych
from Odleglosc import oblicz_macierz_odleglosci
from Losowy import losowy
from Zachlanny import zachlanny, zachlanny_okreslony_start
from SA import symulowane_wyzarzanie
from EA import run_ea

import statistics
import os


def main():
    path = "A/A-n54-k7.vrp"
    
    dane = czytanie_danych(path)
    macierz_odleglosci = oblicz_macierz_odleglosci(dane["node_coords"])

    depot_id = dane["depot"][0]
    lista_klientow = [i for i in dane["demands"].keys() if i != depot_id]   # Warto trzymać jako zmienną, żeby nie odfiltrowywać klientów za każdym razem i mieć jedną przygotowaną listę


    # ---------------------------------------------------
    # Losowy 
    wyniki_losowy = []
    for _ in range(10000):
        koszt_losowy = losowy(dane, macierz_odleglosci, lista_klientow, depot_id)
        wyniki_losowy.append(koszt_losowy)

    print("\nPierwsze 5 wyników algorytmu losowego")
    for i, wynik in enumerate(wyniki_losowy[:5], start=1):
        print(f"{i}: {wynik}")

    best = min(wyniki_losowy)
    worst = max(wyniki_losowy)
    avg = statistics.mean(wyniki_losowy)
    std = statistics.pstdev(wyniki_losowy)

    print("\nStatystyki algorytmu losowego")
    print(f"Liczba prób: {len(wyniki_losowy)}")
    print(f"Najlepszy (min): {best}")
    print(f"Najgorszy (max): {worst}")
    print(f"Średni koszt (avg): {avg:.2f}")
    print(f"Odchylenie standardowe (std): {std:.2f}")
    
    
    
    
    # ---------------------------------------------------
    # Zachłanny od depotu
     
    wyniki_zachlanny = []
    kolejnosc, koszt_zachlanny = zachlanny(dane, macierz_odleglosci, lista_klientow, depot_id)
    wyniki_zachlanny.append(koszt_zachlanny)

    best = min(wyniki_zachlanny)
    worst = max(wyniki_zachlanny)
    avg = statistics.mean(wyniki_zachlanny)
    std = statistics.pstdev(wyniki_zachlanny)

    print("\nZACHLANNY OD DEPOTU:")
    print("Best :", best)
    print("Worst:", worst)
    print("Avg  :", avg)
    print("STD  :", std)
    
    
    
    
    # ---------------------------------------------------
    # Zachłanny z narzyconym startem
    
    wyniki_zachlanny_start = []

    for miasto in lista_klientow:
        k = zachlanny_okreslony_start(dane, macierz_odleglosci, lista_klientow, depot_id, miasto)
        wyniki_zachlanny_start.append(k)

    best_s = min(wyniki_zachlanny_start)
    worst_s = max(wyniki_zachlanny_start)
    avg_s = statistics.mean(wyniki_zachlanny_start)
    std_s = statistics.pstdev(wyniki_zachlanny_start)

    print("\nZACHŁANNY ZE STARTEM:")
    print("Best :", best_s)
    print("Worst:", worst_s)
    print("Avg  :", avg_s)
    print("STD  :", std_s)
    print("\n")
        
    
    
    
    # ---------------------------------------------------
    # SA z zachłannym na start
    
    # parametry SA
    T0 = 100
    Tmin = 0.001
    alpha = 0.98
    iteracje_na_temperature = 50
    rodzaj_ruchu_ile_swap_do_inv = 0.7  # 70% swap, 30% inversion


    wyniki_sa = []
    # zapis CSV z przebiegiem cost vs iteracja 
    csv_path_first = "sa_first_run_iter_vs_cost.csv"

    rodzaj_ruchu = rodzaj_ruchu_ile_swap_do_inv

    for i in range(10):
        print("SA ",i)
        csv_path = csv_path_first if i == 0 else None
        perm, cost, temp_data, gen_bests = symulowane_wyzarzanie(
            dane, macierz_odleglosci, lista_klientow, depot_id,
            T0=T0, Tmin=Tmin, alpha=alpha,
            iteracje=iteracje_na_temperature, rodzaj_ruchu=rodzaj_ruchu,
            csv_path=csv_path, seed=None
        )
        wyniki_sa.append(cost)
        

    print("\nPierwsze 5 wyników SA (koszty końcowe):")
    for idx, k in enumerate(wyniki_sa[:5], start=1):
        print(f"{idx}: {k}")

    best = min(wyniki_sa)
    worst = max(wyniki_sa)
    avg = statistics.mean(wyniki_sa)
    std = statistics.pstdev(wyniki_sa)

    print("\nWYNIKI SA (10 uruchomień) - koszty końcowe:")
    print("Best :", best)
    print("Worst:", worst)
    print("Avg  :", avg)
    print("STD  :", std)

    




    # Parametry EA
    rozmiar_populacji = 250
    liczba_generacji = 800
    rozmiar_turnieju = 7
    prawdopodobienstwo_krzyzowania = 0.6
    prawdopodobienstwo_mutacji = 0.3

    wyniki = []  # najlepsze koszty z każdego uruchomienia
    najlepsze_wyniki = [] # najlepsze osobniki i trasy z runów
    
    folder_wynikow = "wyniki"
    os.makedirs(folder_wynikow, exist_ok=True)
    
    for i in range(10):
        nazwa_pliku = os.path.join(folder_wynikow, f"run_{i+1}.csv")

        naj_osobnik, naj_koszt, naj_trasy = run_ea(
        rozmiar_populacji,
        lista_klientow,
        macierz_odleglosci,
        dane["demands"],
        dane["capacity"],
        depot_id,
        liczba_generacji,
        rozmiar_turnieju,
        prawdopodobienstwo_krzyzowania,
        prawdopodobienstwo_mutacji,
        log_csv_filepath=nazwa_pliku
        )
        
        print("Najlepszy koszt w tym przebiegu:", i, " ", naj_koszt)
        wyniki.append(naj_koszt)
        najlepsze_wyniki.append((naj_koszt, naj_osobnik, naj_trasy))  # zapamiętujemy wynik runa
        
    # dane z 10 wywołań
    najlepszy = min(wyniki)
    najgorszy = max(wyniki)
    srednia = sum(wyniki) / len(wyniki)
    odchylenie = statistics.pstdev(wyniki)  # odchylenie standardowe

    print("\nPo wszystkich uruchomieniach EA:")
    print(f"best:  {najlepszy}")
    print(f"worst: {najgorszy}")
    print(f"avg:   {srednia:.2f}")
    print(f"std:   {odchylenie:.2f}")
    
    for koszt, osobnik, trasy in najlepsze_wyniki:
        if koszt == najlepszy:
            print("\n")
            print("Najlepszy wynik ze wszystkich")
            print("Najlepszy koszt:", koszt)
            print("Najlepszy osobnik:", osobnik)
            print("Najlepsze trasy:", trasy)
            print("")
            break

    
if __name__ == "__main__":
    main()


# Dla zachłannego, aby znać który punkt jest najbliżej magazynu, a który wybrany daje najlepszy wynik
'''
wyniki_zachlanny_start = []

    for miasto in lista_klientow:
        k = zachlanny_okreslony_start(dane, macierz_odleglosci, lista_klientow, depot_id, miasto)
        wyniki_zachlanny_start.append((miasto, k))   # <--- zapamiętujemy też start

    najlepszy_start, best_s = min(wyniki_zachlanny_start, key=lambda x: x[1])
    najgorszy_start, worst_s = max(wyniki_zachlanny_start, key=lambda x: x[1])

    koszty = [k for _, k in wyniki_zachlanny_start]

    avg_s = statistics.mean(koszty)
    std_s = statistics.pstdev(koszty)

    print("\nZACHŁANNY ZE STARTEM:")
    print("Best  :", best_s,  "  (start:", najlepszy_start, ")")
    print("Worst :", worst_s, "  (start:", najgorszy_start,  ")")
    print("Avg   :", avg_s)
    print("STD   :", std_s)
    print("\n")

    najblizsze_miasto = min(lista_klientow, key=lambda c: macierz_odleglosci[depot_id][c])
    odleglosc_min = macierz_odleglosci[depot_id][najblizsze_miasto]

    print("Najbliższe miasto do magazynu:", najblizsze_miasto)
    print("Odległość od magazynu:", odleglosc_min)
    print("Odległość depo → 23:", macierz_odleglosci[depot_id][23])
    print("Odległość depo → 31:", macierz_odleglosci[depot_id][31])
'''