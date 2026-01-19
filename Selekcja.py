# Turniej

import random

def selekcja_turniejowa(oceniona_populacja, rozmiar_turnieju):      # oceniona_populacja - lista krotek (osobnik, koszt, trasy) i rozmiar_turnieju - ile osobników losuje do pojedynczego turnieju
    turniej = random.sample(oceniona_populacja, rozmiar_turnieju)   # Losuje 'rozmiar_turnieju' różnych kandydatów z ocenionej populacji / random.sample , żeby w jednym turnieju nie było duplikatów/ turniej zawiern np. 3 [(osobnik, koszt, trasy),(osobnik, koszt, trasy),(osobnik, koszt, trasy)]

    zwyciezca = turniej[0]                                          # Na razie zakładam, że pierwszy element listy turnieju jest najlepszy / najlepszy[0] to miasta np. [3,5,1,4] (osobnik) / najlepszy[1] to np 1520 (jego koszt) 
    for osobnik, koszt, trasy in turniej:
        if koszt < zwyciezca[1]:                                    # # Jeśli aktualny uczestnik ma mniejszy koszt niż dotychczasowy zwycięzca, to on staje się nowym zwycięzcą.
            zwyciezca = (osobnik, koszt, trasy)

    return zwyciezca # wybrany rodzic (osobnik, koszt, trasy)


'''
Przykład wyniku z main
Zwycięzca turnieju: [20, 23, 7, 30, 17, 32, 16, 29, 11, 25, 5, 22, 28, 10, 12, 4, 24, 3, 9, 8, 13, 31, 21, 27, 14, 2, 19, 18, 15, 26, 6] koszt: 1980
'''