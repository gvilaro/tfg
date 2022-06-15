import abc
from ..campDeBatalla.Posicio import Posicio
from ..campDeBatalla.Tauler import Tauler
from ..campDeBatalla.Moviment import Moviment
from .Rei import Rei
from .Reina import Reina
from .Torre import Torre
from .Alfil import Alfil


class Peca(metaclass=abc.ABCMeta):

    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        self.blanca = blanca
        self.posicio = posicio
        self.morta = morta

    def casellaLegal(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        pecaArribada: Peca = tauler.taulerDeJoc[posicioFinal.fila][posicioFinal.columna]
        if pecaArribada is None:
            return True
        return not pecaArribada.blanca == self.blanca

    def pecaProtegeixDescoberta(self, tauler: Tauler, evitarDescoberta: bool) -> bool:
        tauler.setCasella(self.posicio, None)
        protegeixDescoberta: bool = False
        reiDescobert: Rei = tauler.getRei(self.blanca == evitarDescoberta)
        if self.casellaEnLinea(reiDescobert.posicio):
            if self.recorregutMovimentLliure(tauler, reiDescobert.poscio):
                direccioFilaDescoberta: int = -(self.direccioRecorregut(self.posicio.fila, reiDescobert.posicio.fila))
                direccioColumnaDescoberta: int = -(self.direccioRecorregut(self.posicio.columna, reiDescobert.posicio.columna))
                protegeixDescoberta = self.reiDescobert(tauler, evitarDescoberta, self.posicio, direccioFilaDescoberta, direccioColumnaDescoberta)
        tauler.setCasella(self.posicio, self)
        return protegeixDescoberta

    def reiDescobert(self, tauler: Tauler, evitarDescoberta: bool, posicioAnterior: Posicio, incrementFila: int, incrementColumna: int) -> bool:
        try:
            posicio: Posicio = Posicio(posicioAnterior.fila + incrementFila, posicioAnterior.columna + incrementColumna)
            peca: Peca = tauler.taulerDeJoc[posicio.fila][posicio.columna]
            if peca is None:
                return self.reiDescobert(tauler, evitarDescoberta, posicio, incrementFila, incrementColumna)
            if peca.blanca == (self.blanca == evitarDescoberta):
                return False
            elif (isinstance(peca, Reina)) or (isinstance(peca, Torre)) or (isinstance(peca, Alfil)):
                return peca.escacAlRei(tauler, tauler.getRei(self.blanca == evitarDescoberta).posicio)
            return False
        except Exception:
            return False

    def afegeixMovimentAlJoc(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]):
        movimentActual: Moviment = self.fesMoviment(tauler, posicioFinal)
        tauler.ultimMoviment = movimentActual
        moviments.append(movimentActual)

    def fesMoviment(self, tauler: Tauler, posicioFinal: Posicio) -> Moviment:
        pecaMatada: Peca = tauler.taulerDeJoc[posicioFinal.fila][posicioFinal.columna]
        if not (pecaMatada is None):
            pecaMatada.morta = True
            tauler.setPecesVives(pecaMatada)

        moviment: Moviment = Moviment(self, pecaMatada, self.posicio, posicioFinal)
        self.mouPecaAlTauler(tauler, posicioFinal, moviment)
        return moviment

    def mouPecaAlTauler(self, tauler: Tauler, posicioFinal: Posicio, moviment: Moviment):
        reiContrari: Rei = tauler.getRei(not self.blanca)
        if self.pecaProtegeixDescoberta(tauler, False):
            moviment.escacs = moviment.escacs + 1
            reiContrari.amenacat = True
        tauler.setCasella(self.posicio, None)
        tauler.setCasella(posicioFinal, self)
        self.posicio = posicioFinal
        if self.escacAlRei(tauler, reiContrari.posicio):
            moviment.escacs = moviment.escacs + 1
            reiContrari.amenacat = True

    def direccioRecorregut(self, sortida: int, arribada: int) -> int:
        if sortida - arribada > 0:
            return -1
        elif sortida - arribada < 0:
            return 1
        else:
            return 0

    def recorregutMovimentLliure(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        direccioFila: int = self.direccioRecorregut(self.posicio.fila, posicioFinal.fila)
        direccioColumna: int = self.direccioRecorregut(self.posicio.columna, posicioFinal.columna)

        avancament: int = 1
        moviments: int = abs(self.posicio.fila - posicioFinal.fila)
        if direccioFila == 0:
            moviments: int = abs(self.posicio.columna - posicioFinal.columna)
        while avancament < moviments:
            filaActual: int = self.posicio.fila + (avancament * direccioFila)
            columnaActual: int = self.posicio.columna + (avancament * direccioColumna)
            if tauler.taulerDeJoc[filaActual][columnaActual] is not None:
                return False
            avancament = avancament + 1
        return True

    def casellaEnLinea(self, posicioFinal: Posicio) -> bool:
        return (self.posicio.columna == posicioFinal.columna) or \
               (self.posicio.fila == posicioFinal.fila) or (self.casellaMateixaDiagonal(posicioFinal))

    def casellaMateixaDiagonal(self, posicioFinal: Posicio) -> bool:
        return abs(self.posicio.fila - posicioFinal.fila) == abs(self.posicio.columna - posicioFinal.columna)

    @abc.abstractmethod
    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        pass

    @abc.abstractmethod
    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        pass

    @abc.abstractmethod
    def pecaOfegada(self, tauler: Tauler) -> bool:
        pass

    @abc.abstractmethod
    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        pass

    def afegeixMovimentsPossibles(self, tauler: Tauler, posicioAnterior: Posicio, moviments: [Moviment], incrementFila: int, incrementColumna: int):
        try:
            posicio: Posicio = Posicio(posicioAnterior.fila + incrementFila, posicioAnterior.columna + incrementColumna)
            peca: Peca = tauler.taulerDeJoc[posicio.fila][posicio.columna]
            if peca is None:
                moviments.append(Moviment(self, None, self.posicio, posicio))
                return self.afegeixMovimentsPossibles(tauler, posicio, moviments, incrementFila, incrementColumna)
            elif not (self.blanca == peca.blanca):
                moviments.append(Moviment(self, None, self.posicio, posicio))
        except Exception:
            return

    @abc.abstractmethod
    def imprimeix(self) -> str:
        pass
