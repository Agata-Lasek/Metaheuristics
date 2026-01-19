# pierwsza populacja

import random

def pierwsza_populacja(lista_klientow, rozmiar_populacji):              # działa na liście klientów
    populacja = []                                                      # do przetrzymywania wszystkich osobników

    for i in range(rozmiar_populacji):
        osobnik = random.sample(lista_klientow, len(lista_klientow))    # random.sample losowo miesza listę klientów, tworząc permutację
        populacja.append(osobnik)                                       # na końcu zawsze dodaje osobnika do populacji

    return populacja                                                    # zwraca pierwszą populacje dla EA


'''
from Zachlanny import zachlanny

def pierwsza_populacja(lista_klientow, rozmiar_populacji, dane, macierz, depot):
    populacja = []
    for _ in range(rozmiar_populacji):
        perm, koszt = zachlanny(dane, macierz, lista_klientow, depot)
        populacja.append(perm)
    return populacja
'''