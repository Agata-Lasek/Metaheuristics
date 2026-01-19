import re

def czytanie_danych(sciezka):
    dane = {
        "name": None,
        "dimension": None,
        "capacity": None,
        "node_coords": {},   # współrzędne
        "demands": {},       # demand
        "depot": []
    }

    sekcja = None

    with open(sciezka, "r") as file:
        for linia in file:
            linia = linia.strip()

            if not linia or linia == "EOF":
                continue

            if linia.startswith("NAME"):
                dane["name"] = linia.split(":")[1].strip()
            elif linia.startswith("DIMENSION"):
                dane["dimension"] = int(linia.split(":")[1].strip())
            elif linia.startswith("CAPACITY"):
                dane["capacity"] = int(linia.split(":")[1].strip())
            elif linia.startswith("NODE_COORD_SECTION"):
                sekcja = "node_coords"
                continue
            elif linia.startswith("DEMAND_SECTION"):
                sekcja = "demands"
                continue
            elif linia.startswith("DEPOT_SECTION"):
                sekcja = "depot"
                continue

            elif sekcja == "node_coords":
                parts = linia.split()
                if len(parts) >= 3:
                    idx, x, y = parts[:3]
                    dane["node_coords"][int(idx)] = (float(x), float(y))

            elif sekcja == "demands":
                parts = linia.split()
                if len(parts) >= 2:
                    idx, demand = parts[:2]
                    dane["demands"][int(idx)] = int(demand)

            # Depot
            elif sekcja == "depot":
                if linia == "-1":
                    sekcja = None
                else:
                    dane["depot"].append(int(linia))

    return dane


'''
wygląd danych:

dane = {
    "name": "A-n32-k5",
    "dimension": 32,
    "capacity": 100,
    "node_coords": { 1: (82,76), 2: (96,44), 3: (50,5), ... },
    "demands":    { 1: 0, 2: 19, 3: 21, ... },
    "depot":      [1]
}
'''