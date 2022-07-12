from . import Peca, Rei
from ..campDeBatalla import Tauler, Posicio, Moviment


class Reina(Peca):

    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)

    'mètode redefinit'
    def casellaLegal(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if super().casellaLegal(tauler, posicioFinal):
            return self.casellaEnLineaDeReina(posicioFinal)
        return False

    def casellaEnLineaDeReina(self, posicioFinal: Posicio):
        distanciaFila: int = abs(self.posicio.fila - posicioFinal.fila)
        distanciaColumna: int = abs(self.posicio.columna - posicioFinal.columna)
        return (distanciaFila - distanciaColumna == 0) or (distanciaFila * distanciaColumna == 0)

    'sobrecàrrega mètode'
    def pecaProtegeixDescoberta(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if super().pecaProtegeixDescoberta(tauler, True):
            return self.recorregutDesprotegeixRei(tauler, posicioFinal)
        return False

    def recorregutDesprotegeixRei(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        reiPropi: Rei = tauler.getRei(self.blanca)
        if self.posicio.fila == reiPropi.posicio.fila:
            return not self.posicio.fila == posicioFinal.fila
        elif self.posicio.columna == reiPropi.posicio.columna:
            return not self.posicio.columna == posicioFinal.columna
        else:
            return not (self.casellaMateixaDiagonal(posicioFinal) and \
                   reiPropi.casellaMateixaDiagonal(posicioFinal))

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal):
            return False
        if self.pecaProtegeixDescoberta(tauler, posicioFinal):
            return False
        if self.recorregutMovimentLliure(tauler, posicioFinal):
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            return True
        return False

    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        return self.casellaEnLineaDeReina(posicioReiRival) and self.recorregutMovimentLliure(tauler, posicioReiRival)

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        moviments: [Moviment] = []
        if super().pecaProtegeixDescoberta(tauler, True):
            moviments.extend(self.movimentsPossiblesEnLineaDescoberta(tauler, True, 1))
            moviments.extend(self.movimentsPossiblesEnLineaDescoberta(tauler, True, -1))
            return moviments
        for direccioFila in range(-1, 2):
            for direccioColumna in range(-1, 2):
                self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, direccioFila, direccioColumna)
        return moviments

    def imprimeix(self) -> str:
        if self.blanca:
            return 'D'
        else:
            return 'd'
