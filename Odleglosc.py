import math

def oblicz_macierz_odleglosci(node_coords):

    # Zwraca słownik distances[i][j] = odległość między i i j

    distances = {}                                      # tworzy pustą strukturę do zapisywania macierzy odległości
    for i in node_coords.keys():
        distances[i] = {}                               # pusty słownik, w którym będzą trzymane wszystkie odległości

    for i, (x1, y1) in node_coords.items():             # Podwójna pętla przechodzi po wszystkich punktach
        for j, (x2, y2) in node_coords.items():
            dx, dy = x1 - x2, y1 - y2                   # Oblicza różnicę współrzędnych między punktami i i j
            distances[i][j] = round(math.hypot(dx, dy)) # math.hypot(dx, dy) liczy odległość Euklidesową, krótszy zapis: (math.sqrt(dx*dx + dy*dy)), distances[i][j] = obliczona_odległość, round zaokrągla do całkowitej

    return distances                                    # zwraca macierz_odleglosci

'''
wygląd macierzy_odleglosci

distances = {
    1: {1: 0, 2: 28, 3: 55},
    2: {1: 28, 2: 0, 3: 41},
    3: {1: 55, 2: 41, 3: 0}
}
'''