
#main do sprawdzania (pomocny)
# 
from dane import czytanie_danych
from Odleglosc import oblicz_macierz_odleglosci
from Populacja import pierwsza_populacja
from Ocena import ocen_populacje
from Najlepszy import znajdz_najlepszy_w_populacji
from Selekcja import selekcja_turniejowa
from Krzyzowanie import krzyzowanie_OX
from Mutacja import mutacja_swap, mutacja_inwersja

def main():
    path = "A/A-n32-k5.vrp"
    
    dane = czytanie_danych(path)
    macierz_odleglosci = oblicz_macierz_odleglosci(dane["node_coords"])

    depot_id = dane["depot"][0]
    lista_klientow = [i for i in dane["demands"].keys() if i != depot_id]   # Warto trzymać jako zmienną, żeby nie odfiltrowywać klientów za każdym razem i mieć jedną przygotowaną listę




    # Parametry EA
    rozmiar_populacji = 10
    liczba_generacji = 5
    rozmiar_turnieju = 3
    prawdopodobienstwo_krzyzowania = 0.7
    prawdopodobienstwo_mutacji = 0.6


    # tworzenie pierwszej losowej populacji
    populacja = pierwsza_populacja(lista_klientow, rozmiar_populacji)

    oceniona_populacja = ocen_populacje(populacja, macierz_odleglosci, dane["demands"], dane["capacity"], depot_id)

    print("\nWyniki oceny (osobnik : koszt):")
    for osobnik, koszt, trasa in oceniona_populacja[:3]:
        print(osobnik, " -> koszt:", koszt,  " -> trasy:", trasa)

    najlepszy_osobnik, najlepszy_koszt, najlepsza_trasa = znajdz_najlepszy_w_populacji(oceniona_populacja)
    print("\nNajlepszy koszt:", najlepszy_koszt)
    print("Najlepszy osobnik:", najlepszy_osobnik)
    print("Najlepsza trasa:", najlepsza_trasa)
    
    zwyciezca, koszt, naj_trasa = selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju)
    print("Zwycięzca turnieju:", zwyciezca, "koszt:", koszt, "\ntrasa:", naj_trasa)
    
    rodzic1, koszt1, trasa1 = selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju)
    rodzic2, koszt2, trasa2 = selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju)
    
    dziecko, poczatek, koniec = krzyzowanie_OX(rodzic1, rodzic2, prawdopodobienstwo_krzyzowania)

    if poczatek is None:
        print("Krzyżowanie nie zaszło – zwrócono kopię rodzica1")
        print("\nRodzic1:      ", rodzic1)
        print("\nDziecko:      ", dziecko)
    else:
        print("\nRodzic1:      ", rodzic1)
        print("\nRodzic2:      ", rodzic2)
        print("\nFragment z R1:", rodzic1[poczatek:koniec+1])
        print(f"Indeksy cięcia: {poczatek} do {koniec}")
        print("\nDziecko:      ", dziecko)
        
    zmutowane_dziecko = mutacja_inwersja(dziecko, prawdopodobienstwo_mutacji)
    print("\nPo mutacji:  ", zmutowane_dziecko)
    


if __name__ == "__main__":
    main()
