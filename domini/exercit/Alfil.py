from .Peca import Peca
from .Rei import Rei
from ..campDeBatalla.Moviment import Moviment
from ..campDeBatalla.Posicio import Posicio
from ..campDeBatalla.Tauler import Tauler


class Alfil(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal):
            return False
        if not self.casellaMateixaDiagonal(posicioFinal) or self.pecaProtegeixDescoberta(tauler, posicioFinal):
            return False
        if self.recorregutMovimentLliure(tauler, posicioFinal):
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            return True
        return False

    'sobrecàrrega mètode'
    def pecaProtegeixDescoberta(self, tauler: Tauler, posicioFinal: Posicio):
        if super().pecaProtegeixDescoberta(tauler, True):
            reiContrari: Rei = tauler.getRei(self.blanca)
            return not (self.casellaMateixaDiagonal(reiContrari.posicio)
                        and reiContrari.casellaMateixaDiagonal(posicioFinal))
        return False

    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        return self.casellaMateixaDiagonal(posicioReiRival) and self.recorregutMovimentLliure(tauler, posicioReiRival)

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        moviments: [Moviment] = []
        if super().pecaProtegeixDescoberta(tauler, True):
            reiPropi: Rei = tauler.getRei(self.blanca)
            direccioFila: int = self.direccioRecorregut(self.posicio.fila, reiPropi.posicio.fila)
            direccioColumna: int = self.direccioRecorregut(self.posicio.columna, reiPropi.posicio.columna)
            self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, direccioFila, direccioColumna)
            self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, -direccioFila, -direccioColumna)
            return moviments
        for fila in [-1, 1]:
            for columna in [-1, 1]:
                self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, fila, columna)
        return moviments

    def imprimeix(self) -> str:
        if self.blanca:
            return 'A'
        else:
            return 'a'
