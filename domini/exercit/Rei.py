from .Peca import Peca
from .Torre import Torre
from ..campDeBatalla.Tauler import Tauler
from ..campDeBatalla.Posicio import Posicio
from ..campDeBatalla.Moviment import Moviment


class Rei(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)
        self.amenacat = False
        self.enrocament = True

    def casellaAmenacada(self, tauler: Tauler, posicio: Posicio) -> bool:
        colorRival: bool = not self.blanca
        for peca in tauler.getPecesVives(colorRival):
            if peca.escacAlRei(tauler, posicio):
                return True
        return False

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal):
            return False

        movimentValid: bool = False
        x: int = abs(self.posicio.fila - posicioFinal.fila)
        y: int = abs(self.posicio.columna - posicioFinal.columna)
        if (x * y) < 2:
            movimentValid = not self.casellaAmenacada(tauler, posicioFinal)
        elif self.esEnrocament(tauler, posicioFinal):
            if self.enrocaAlRei(tauler, posicioFinal):
                movimentValid = True
                self.avisaTorreEnrocada(tauler, posicioFinal, moviments)
        if movimentValid:
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            self.enrocament = False
            self.amenacat = False
        return movimentValid

    def esEnrocament(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if not self.enrocament or self.amenacat:
            return False
        if (self.posicio.fila == posicioFinal.fila) and (posicioFinal.fila == 0 or posicioFinal.fila == 7) and \
                (posicioFinal.columna == 6 or posicioFinal.columna == 2):
            return self.torrePermetEnrocament(tauler, posicioFinal)
        return False

    def torrePermetEnrocament(self, tauler: Tauler, posicioFinal: Posicio):
        if posicioFinal.columna == 2:
            torreEnrocament: Peca = tauler.taulerDeJoc[posicioFinal.fila][0]
        else:
            torreEnrocament: Peca = tauler.taulerDeJoc[posicioFinal.fila][7]
        if isinstance(torreEnrocament, Torre) and not torreEnrocament.moguda:
            return True
        return False

    def enrocaAlRei(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        recorregut: range = self.recorregutEnrocament(posicioFinal)
        for columna in recorregut:
            if not tauler.esCasellaBuida(posicioFinal) or \
                    self.casellaAmenacada(tauler, Posicio(posicioFinal.fila, columna)):
                return False
        return True

    def recorregutEnrocament(self, posicioFinal: Posicio) -> range:
        if posicioFinal.columna == 6:
            return range(5, 7)
        else:
            return range(2, 4)

    def avisaTorreEnrocada(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]):
        if posicioFinal.columna == 2:
            torreEnrocada: Torre = tauler.taulerDeJoc[self.posicio.fila][0]
            posicioFinalTorre: Posicio = Posicio(self.posicio.fila, 3)
        else:
            torreEnrocada: Torre = tauler.taulerDeJoc[self.posicio.fila][7]
            posicioFinalTorre: Posicio = Posicio(self.posicio.fila, 5)
        torreEnrocada.afegeixMovimentAlJoc(tauler, posicioFinalTorre, moviments)

    def escacMat(self, tauler: Tauler) -> bool:
        if self.pecaOfegada(tauler):
            self.morta = True
            return True
        else:
            return False

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        movimentsPossibles = [Moviment]
        for fila in range(self.posicio.fila + 1, self.posicio.fila - 2):
            for columna in range(self.posicio.columna + 1, self.posicio.columna - 2):
                try:
                    posicio: Posicio = Posicio(fila, columna)
                    if self.casellaLegal(tauler, posicio) and not self.casellaAmenacada(tauler, posicio):
                        movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
                except IndexError:
                    {}
        self.afegirMovimentsEnrocament(tauler, movimentsPossibles)
        return movimentsPossibles

    def afegirMovimentsEnrocament(self, tauler: Tauler, movimentsPossibles: [Moviment]):
        if self.enrocament and not self.amenacat:
            enrocamentCurt: Posicio = Posicio(self.posicio.fila, 6)
            enrocamentLlarg: Posicio = Posicio(self.posicio.fila, 2)
            for enrocament in [enrocamentCurt, enrocamentLlarg]:
                if self.torrePermetEnrocament(tauler, enrocament) and self.enrocaAlRei(tauler, enrocament):
                    movimentsPossibles.append(Moviment(self, None, self.posicio, enrocament))
            self.enrocament = True

    def pecaOfegada(self, tauler: Tauler) -> bool:
        for fila in range(self.posicio.fila + 1, self.posicio.fila - 2):
            for columna in range(self.posicio.columna + 1, self.posicio.columna - 2):
                try:
                    posicio: Posicio = Posicio(fila, columna)
                    if self.casellaLegal(tauler, posicio) and not self.casellaAmenacada(tauler, posicio):
                        return False
                except IndexError:
                    {}
        return True

    def escacAlRei(self, tauler: Tauler, possibleSortidaReiRival: Posicio) -> bool:
        x: int = abs(self.posicio.fila - possibleSortidaReiRival.fila)
        y: int = abs(self.posicio.columna - possibleSortidaReiRival.columna)
        return (x * y) < 2

    def imprimeix(self) -> str:
        if self.blanca:
            return 'K'
        else:
            return 'k'

