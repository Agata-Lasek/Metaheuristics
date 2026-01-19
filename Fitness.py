# funkcja fitness

def podzial_na_trasy(osobnik, demands, capacity):
    # Dzieli permutację klientów na listę tras zgodnie z pojemnością
    trasy = []              # lista wszystkich tras (wynik)
    trasa = []              # aktualnie budowana trasa
    aktualny_ladunek = 0

    for klient in osobnik:
        zapotrzebowanie = demands[klient]           # ile klient potrzebuje
        if aktualny_ladunek + zapotrzebowanie > capacity:
            # Jeśli dodanie tego klienta przekroczy pojemność pojazdu, zakończ bieżącą trasę i zacznij nową z tym klientem
            trasy.append(trasa)                     # zapisuje zakończoną trasę
            trasa = [klient]                        # nowa trasa od tego klienta
            aktualny_ladunek = zapotrzebowanie      # reset ładunku do zapotrzebowania tego klienta
        else:
            trasa.append(klient)                    # Można dodać klienta
            aktualny_ladunek += zapotrzebowanie     # zwiększenie wydanego ładunku

    if trasa:                                       # jeśli ostatnia trasa jest niepusta, dodaje ją do listy tras
        trasy.append(trasa)
    return trasy                                    # Zwraca liste tras


def fitness(osobnik, distances, demands, capacity, depot_id):

    trasy = podzial_na_trasy(osobnik, demands, capacity)

    koszt = 0                                       # akumuluje łączny koszt
    for trasa in trasy:                             # Dla każdej trasy licze długość/koszt
        poprzedni = depot_id                        # start z depotu
        for klient in trasa:
            koszt += distances[poprzedni][klient]   # dodaje odległość z poprzedniego punktu do obecnego klienta, na start poprzedni to depot
            poprzedni = klient                      # przesuwam poprzedni po każdym
        koszt += distances[poprzedni][depot_id]     # po przejechaniu wszystkich klientów powrót do depo

    return koszt, trasy                             # zwraca sume długości wszystkich tras i trasy
