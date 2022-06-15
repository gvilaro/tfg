from ..campDeBatalla.Moviment import Moviment
from ..campDeBatalla.Posicio import Posicio
from ..campDeBatalla.Tauler import Tauler
from .Peca import Peca


class Cavall(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal) or self.pecaProtegeixDescoberta(tauler, True):
            return False
        x: int = abs(self.posicio.fila - posicioFinal.fila)
        y: int = abs(self.posicio.fila - posicioFinal.fila)
        if x * y == 2:
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            return True
        return False

    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        x: int = abs(self.posicio.fila - posicioReiRival.fila)
        y: int = abs(self.posicio.fila - posicioReiRival.fila)
        return x * y == 2

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        moviments: [Moviment] = []
        if self.pecaProtegeixDescoberta(tauler, True):
            return moviments
        for i in [-2, 2]:
            for y in [-1, 1]:
                try:
                    posicio: Posicio = Posicio(i, y)
                    if self.casellaLegal(tauler, posicio):
                        moviments.append(Moviment(self, None, self.posicio, posicio))
                    posicio = Posicio(y, i)
                    if self.casellaLegal(tauler, posicio):
                        moviments.append(Moviment(self, None, self.posicio, posicio))
                except IndexError:
                    {}
        return moviments

    def imprimeix(self) -> str:
        if self.blanca:
            return 'C'
        else:
            return 'c'
