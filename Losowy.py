import random
from Fitness import fitness

    #Funkcja tworzy losowego osobnika, oblicza koszt jego trasy i zwraca tylko koszt
    
def losowy(dane, macierz, klienci, depot):
    if isinstance(depot, list):
        depot = depot[0]                            # magazyn mam jako lista(na przyszłość), pobieram jego pierwszy element

    perm = random.sample(klienci, len(klienci))     # Generuje losową permutację klientów bez powtórzeń
    koszt, _ = fitness(perm, macierz, dane["demands"], dane["capacity"], depot)      # Obliczam koszt permutacji przez fitness, nie potrzebuje na razie podziału na trasy
    return koszt    # dostaje tylko koszt
