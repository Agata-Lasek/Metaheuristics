# Ordered Crossover

import random

def krzyzowanie_OX(rodzic1, rodzic2, prawdopodobienstwo):

    if random.random() > prawdopodobienstwo:            # Losuje czy wykonać krzyżowanie
        return rodzic1.copy(), None, None               # Brak krzyżowania, zwracana kopia rodzica1 i brak cięcia
    
    dlugosc = len(rodzic1)

    poczatek = random.randint(0, dlugosc - 2)           # Dwa punkty cięcia w jednym osobniku rodzicielskim
    koniec = random.randint(poczatek + 1, dlugosc - 1)

    dziecko = [None] * dlugosc                          # Tworze puste dziecko, bo potrzebuje szablonu, żeby włożyć fragment od rodzica1, a potem uzupełnić resztę z rodzica2 w dobrej kolejności

    for i in range(poczatek, koniec + 1):               # Przepisuje fragment z rodzica1 do dziecka
        dziecko[i] = rodzic1[i]

    indeks_rodzica2 = 0                                 # Uzupełniam resztę genami z rodzica2 (kolejność zachowana)
    for i in range(dlugosc):
        if dziecko[i] is None:
            
            while rodzic2[indeks_rodzica2] in dziecko:  # Szukam kolejnej wartości z rodzica2, której jeszcze nie ma w dziecku
                indeks_rodzica2 += 1
            dziecko[i] = rodzic2[indeks_rodzica2]

    return dziecko, poczatek, koniec                    # początek i koniec tylko do wyświetlenia punktu cięcia, normalnie zwracam tylko dziecko


'''
Przykład wyniku z main

Rodzic1:       [23, 18, 12, 32, 22, 20, 26, 21, 7, 15, 16, 24, 3, 13, 25, 4, 14, 2, 31, 10, 28, 30, 29, 6, 5, 17, 11, 27, 19, 9, 8]

Rodzic2:       [27, 4, 2, 8, 29, 19, 10, 17, 18, 23, 24, 32, 12, 15, 9, 26, 14, 7, 30, 5, 31, 13, 28, 20, 3, 11, 22, 25, 21, 6, 16]

Fragment z R1: [22, 20]
Indeksy cięcia: 4 do 5

Dziecko:       [27, 4, 2, 8, 22, 20, 29, 19, 10, 17, 18, 23, 24, 32, 12, 15, 9, 26, 14, 7, 30, 5, 31, 13, 28, 3, 11, 25, 21, 6, 16]
'''