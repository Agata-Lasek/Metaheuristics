# przechodzę po całej populacji i liczę fitness każdemu osobnikowi

from Fitness import fitness

def ocen_populacje(populacja, distances, demands, capacity, depot):
    wyniki = []                                                              # lista na ocenione osobniki

    for osobnik in populacja:                                                # dla każdego
        koszt, trasy = fitness(osobnik, distances, demands, capacity, depot) # fitness zwraca koszt rozwiązania i podział miast na trasy
        wyniki.append( (osobnik, koszt, trasy) )                             # # zapisuje ocenę osobnika razem z trasami

    return wyniki           # zwracam ocenioną populację
