from Fitness import fitness

def zachlanny(dane, macierz_odleglosci, lista_klientow, depot):
    if isinstance(depot, (list, tuple)):
        depot = depot[0]

    zapotrzebowanie = dane["demands"]
    pojemnosc = dane["capacity"]

    nieobsluzeni = set(lista_klientow)
    kolejnosc_klientow = []

    while nieobsluzeni:
        aktualne_miasto = depot
        aktualne_obciazenie = 0

        while True:
            mozliwi_klienci = [
                klient for klient in nieobsluzeni
                if aktualne_obciazenie + zapotrzebowanie[klient] <= pojemnosc
            ]

            if not mozliwi_klienci:
                break

            najblizszy_klient = min(
                mozliwi_klienci,
                key=lambda klient: macierz_odleglosci[aktualne_miasto][klient]
            )

            kolejnosc_klientow.append(najblizszy_klient)
            nieobsluzeni.remove(najblizszy_klient)
            aktualne_obciazenie += zapotrzebowanie[najblizszy_klient]
            aktualne_miasto = najblizszy_klient

    koszt, _ = fitness(kolejnosc_klientow, macierz_odleglosci, zapotrzebowanie, pojemnosc, depot)
    return kolejnosc_klientow, koszt






def zachlanny_okreslony_start(dane, macierz, klienci, depot, start):
    if isinstance(depot, list):
        depot = depot[0]                # magazyn mam jako lista(na przyszłość), pobieram jego pierwszy element

    unserved = set(klienci)             # Zbiór klientów, którzy nie są obsłużeni
    perm = []                           # Tworzona permutacja
    demands = dane["demands"]           # Moje zapotrzebowanie i pojemność pojazdu
    cap = dane["capacity"]

    while unserved:                     # dopóki istnieją nieobsłużeni
        aktualne_miasto = depot         # na start aktualny miasto to magazyn, ale magazyn nie jest dopisywany do listy, to się dzieje w fitness
        aktualne_obciazenie = 0         # na start ładunek na 0 (potem porównam z capacity za kazdym razem) robie od drugiej strony jakbym zbierała zz miast

        if start in unserved and demands[start] <= cap: # Jeśli klient startowy jest do obsłużenia i zapotrzebowanie mieści się w pojemności pojazdu
            perm.append(start)                          # dodaje go do trasy
            unserved.remove(start)                      # usuwam z nieobsłużonych
            aktualne_obciazenie += demands[start]       # aktualizuje ładunek
            aktualne_miasto = start                     # ustawiam jako aktualne miasto (ostatnie odwiedzone)

        while True:                                     # Szukam kolejnych klientów (miasta), opiz w # Jak to działa
            mozliwi_klienci = [                         # których można jeszcze dodać bez przekraczania pojemności
                klient for klient in unserved 
                if aktualne_obciazenie + demands[klient] <= cap
            ]
            
            if not mozliwi_klienci:                     # Jeśli nie ma takich, kończe trasę
                break
            
            n = min(mozliwi_klienci, key=lambda x: macierz[aktualne_miasto][x]) # Wybieram najbliższego aktualnemu punktowi
            perm.append(n)                                                      # aktualizuje stan
            unserved.remove(n)
            aktualne_obciazenie += demands[n]
            aktualne_miasto = n

    koszt, _ = fitness(perm, macierz, demands, cap, depot)  # Po stworzeniu pełnej permutacji obliczam jej koszt przez fitness
    return koszt    # dostaje tylko koszt

# Jak to działa
# Filtruje klientów, którzy zmieszczą się w ciężarówce
# Dopiero z przefiltrowanej listy wybieram najbliższego sąsiada