from Populacja import pierwsza_populacja
from Ocena import ocen_populacje
from Najlepszy import znajdz_najlepszy_w_populacji
from Selekcja import selekcja_turniejowa
from Krzyzowanie import krzyzowanie_OX
from Mutacja import mutacja_swap, mutacja_inwersja

import csv
import statistics

def run_ea(rozmiar_populacji, lista_klientow, distances, demands, capacity, depot_id,
           liczba_generacji, rozmiar_turnieju, prawdopodobienstwo_krzyzowania, prawdopodobienstwo_mutacji, log_csv_filepath=None):

    # tworzenie pierwszej losowej populacji
    populacja = pierwsza_populacja(lista_klientow, rozmiar_populacji) 

    # tworzenie pierwszej zachłannej populacji (do zachłannej odkomentować poniższą linijkę) ALE wszystkie osobniki takie same
    '''populacja = pierwsza_populacja(lista_klientow, rozmiar_populacji, dane, distances, depot_id)'''
    
    # jeśli mam log do CSV, zapisz nagłówek (nadpisze plik) / to się zajmuje zapisem statystyk do csv
    if log_csv_filepath is not None:
        with open(log_csv_filepath, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["generacja", "best_cost", "avg_cost", "worst_cost"])
            

    for gen in range(0, liczba_generacji):                                                      # Pętla główna, która iteruje po generacjach
        oceniona_populacja = ocen_populacje(populacja, distances, demands, capacity, depot_id)  # dla populacji w generacji oblicza funkcje celu dla każdego osobnika i zwraca (osobnik, koszt, trasy) 
        
        # wyciągam tylko koszty, best, avg, worst do statystyk aby wiedzieć jak radzi sobie populacja, zapisuje to potem do csv
        koszty = [koszt for (_, koszt, _) in oceniona_populacja]
        best = min(koszty)
        worst = max(koszty)
        avg = statistics.mean(koszty)

        # zapis powyższych statystyk do CSV - potem z tego wykres na koniec
        if log_csv_filepath is not None:
            with open(log_csv_filepath, mode="a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([gen+1, best, round(avg, 6), worst])

        # szukam najlepszego w mojej generacji i zapamietuje, później dodam go jako możliwego rodzica do nastepnej generacji
        najlepszy_osobnik_w_generacji, najlepszy_koszt_w_generacji, najlepsze_trasy_w_generacji  = znajdz_najlepszy_w_populacji(oceniona_populacja)

        nowe_pokolenie = []                                         # robię miejsce na nowe pokolenie, to bedzie populacja w nastepnej generacji
        nowe_pokolenie.append(najlepszy_osobnik_w_generacji)        # dodaje wczesniej znalezionego najlepszego osobnika do nastepnego pokolenia

        while len(nowe_pokolenie) < rozmiar_populacji:              # dopuki nie otrzymam tylu nowych osobników ile było na początku/ zawsze chcę mieć 100 osobników

            rodzic1, koszt1, trasa1 = selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju)                         # wybieram dwóch rodziców przez turniej
            rodzic2, koszt2, trasa2 = selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju)                         # dalej korzystam tylko z rodzic1/rodzic2 ale selekcja zwraca krotkę (osobnik, koszt, trasy)

            dziecko, poczatek, koniec = krzyzowanie_OX(rodzic1, rodzic2, prawdopodobienstwo_krzyzowania)                # próbuje robić krzyżowanie ale funkcja może zwrócić kopię rodzica, jeśli krzyżowanie nie zajdzie, zależy od prawdopodobieństwa

            dziecko_po_mutacji = mutacja_inwersja(dziecko, prawdopodobienstwo_mutacji)  # z dziecka, albo rodzica jesli nie było krzyzowania prubuję mutowac z pewnym prawdopodobieństwem, robię jedną z mutacji swap albo inwersję (teraz jest inwersja - zmieniam w kodzie)

            nowe_pokolenie.append(dziecko_po_mutacji)                                   # dziecko po krzyzowaniu i mutacji, albo bez dodaję do następnego pokolenia

        populacja = nowe_pokolenie                                                      # zastąpienie starej populacji nową (czyli w nastepnej generacji to tą będę oceniać)

    oceniona_koncowa = ocen_populacje(populacja, distances, demands, capacity, depot_id)                                    # po wszystkich generacjach oceń ostatnią populację
    najlepszy_osobnik_koncowy, najlepszy_koszt_koncowy, najlepsze_trasy  = znajdz_najlepszy_w_populacji(oceniona_koncowa)   # po wszystkich generacjach wybierz najlepszego

    return najlepszy_osobnik_koncowy, najlepszy_koszt_koncowy, najlepsze_trasy                                              # zwraca najlepsze znalezione rozwiązanie
