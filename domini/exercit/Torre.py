from .Peca import Peca
from .Rei import Rei
from ..campDeBatalla import Tauler, Posicio, Moviment


class Torre(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)
        self.moguda = False

    'mètode redefinit'
    def casellaLegal(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if super().casellaLegal(tauler, posicioFinal):
            return self.casellaEnLineaDeTorre(posicioFinal)
        return False

    def casellaEnLineaDeTorre(self, posicioFinal: Posicio):
        return self.posicio.fila == posicioFinal.fila \
               or self.posicio.columna == posicioFinal.columna

    'sobrecàrrega mètode'
    def pecaProtegeixDescoberta(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        reiPropi: Rei = tauler.getRei(self.blanca)
        if super().pecaProtegeixDescoberta(tauler, True):
            return not ((self.posicio.fila == reiPropi.posicio.fila == posicioFinal.fila)
                        or (self.posicio.columna == reiPropi.posicio.columna == posicioFinal.columna))
        return False

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal) or self.pecaProtegeixDescoberta(tauler, posicioFinal):
            return False
        if self.recorregutMovimentLliure(tauler, posicioFinal):
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            self.moguda = True
            return True
        return False

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        return self.casellaEnLineaDeTorre(posicioReiRival) and self.recorregutMovimentLliure(tauler, posicioReiRival)

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        moviments: [Moviment] = []
        if super().pecaProtegeixDescoberta(tauler, True):
            reiPropi: Rei = tauler.getRei(self.blanca)
            direccioFila: int = self.direccioRecorregut(self.posicio.fila, reiPropi.posicio.fila)
            direccioColumna: int = self.direccioRecorregut(self.posicio.columna, reiPropi.posicio.columna)
            self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, direccioFila, direccioColumna)
            self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, -direccioFila, -direccioColumna)
            return moviments
        for i in range(2):
            for direccioMoviment in [-1, 1]:
                self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, 0, direccioMoviment)
                self.afegeixMovimentsPossibles(tauler, self.posicio, moviments, direccioMoviment, 0)
        return moviments

    def imprimeix(self) -> str:
        if self.blanca:
            return 'T'
        else:
            return 't'



