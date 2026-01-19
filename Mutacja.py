import random

def mutacja_swap(dziecko, prawdopodobienstwo):
    
    if random.random() > prawdopodobienstwo:        # czy mutacja zajdzie
        return dziecko                              # nic nie zmieniam

    i = random.randint(0, len(dziecko) - 1)         # losuje dwa różne indeksy
    j = random.randint(0, len(dziecko) - 1)
    while j == i:
        j = random.randint(0, len(dziecko) - 1)     # upewniam się, że nie wylosuje 2 razy tego samego miejsca

    tymczasowe = dziecko[i]                         # zamieniam miejscami
    dziecko[i] = dziecko[j]
    dziecko[j] = tymczasowe

    return dziecko

'''
Przykladowy wynik swap
Dziecko:       [27, 4, 2, 8, 22, 20, 29, 19, 10, 17, 18, 23, 24, 32, 12, 15, 9, 26, 14, 7, 30, 5, 31, 13, 28, 3, 11, 25, 21, 6, 16]
Po mutacji:   [27, 4, 2, 8, 22, 20, 29, 19, 10, 17, 18, 23, 24, 32, 26, 15, 9, 12, 14, 7, 30, 5, 31, 13, 28, 3, 11, 25, 21, 6, 16]

W tym przykladzie 12 i 26 zamienione
'''



def mutacja_inwersja(dziecko, prawdopodobienstwo):

    if random.random() > prawdopodobienstwo:        # czy mutacja zajdzie
        return dziecko

    i = random.randint(0, len(dziecko) - 1)         # losuje dwa różne indeksy
    j = random.randint(0, len(dziecko) - 1)
    while j == i:
        j = random.randint(0, len(dziecko) - 1)     # upewniam się, że nie wylosuje 2 razy tego samego miejsca

    if i > j:                                       # upewniam się, że indeks i < j
        i, j = j, i

    fragment = dziecko[i:j+1]                       # odwracam fragment między i a j
    fragment.reverse()
    dziecko[i:j+1] = fragment

    return dziecko

'''
Przykladowy wynik swap
Dziecko:       [29, 8, 4, 6, 27, 3, 15, 23, 2, 14, 17, 13, 31, 22, 5, 21, 28, 9, 10, 30, 26, 11, 20, 19, 32, 16, 24, 12, 25, 18, 7]
Po mutacji:   [29, 8, 4, 6, 27, 3, 15, 23, 2, 14, 17, 13, 18, 25, 12, 24, 16, 32, 19, 20, 11, 26, 30, 10, 9, 28, 21, 5, 22, 31, 7]

W tym przykladzie 18 i 31 są wybrane
'''