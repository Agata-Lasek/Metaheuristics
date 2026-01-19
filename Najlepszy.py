
def znajdz_najlepszy_w_populacji(oceniona_populacja):
    najlepszy = oceniona_populacja[0]                   # zakładam na początek, że pierwszy jest najlepszy / każdy element to: (osobnik, koszt, trasy)
    for osobnik, koszt, trasy in oceniona_populacja:    # Przechodzę po wszystkich ocenionych elementach; każdy element to (osobnik,koszt,trasy)
        if koszt < najlepszy[1]:                        # porównuje koszty / najlepszy[0] to miasta np. [3,5,1,4] (osobnik) / najlepszy[1] to np 1520 (jego koszt)
            najlepszy = (osobnik, koszt, trasy)         # Jeśli jest mniejszy to aktualizuje najlepszego
    return najlepszy                                    # Zwracam krotkę (osobnik, koszt, trasy) z najlepszym w populacji
