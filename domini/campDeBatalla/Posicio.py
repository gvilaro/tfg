class Posicio:

    def __init__(self, fila: int, columna: int):
        self.comprovaPosicio(fila, columna)
        self.fila = fila
        self.columna = columna

    def comprovaPosicio(self, fila: int, columna: int):
        if fila < 0 or fila > 7 or columna < 0 or columna > 7:
            raise IndexError("La posició final indicada està fora del tauler")
        'if (fila or columna) < 0 or (fila or columna) > 7:'






