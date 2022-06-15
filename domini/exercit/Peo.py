from random import random

from .Peca import Peca
from .Reina import Reina
from .Torre import Torre
from .Alfil import Alfil
from .Cavall import Cavall

from ..campDeBatalla.Tauler import Tauler
from ..campDeBatalla.Posicio import Posicio
from ..campDeBatalla.Moviment import Moviment


class Peo(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)
        self.moguda = False

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal):
            return False

        pasEndavant: int = self.posicio.fila - posicioFinal.fila
        if self.peoVaEnrere(pasEndavant) or self.pecaProtegeixDescoberta(tauler, True):
            return False

        movimentValid: bool = False
        if abs(pasEndavant) == 1:
            if self.posicio.columna == posicioFinal.columna:
                movimentValid = True
            else:
                movimentValid = self.mataPecaRival(tauler, posicioFinal)
        elif abs(pasEndavant) == 2:
            movimentValid = self.moure2caselles(tauler)
        if movimentValid:
            self.moguda = True
            self.afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
        return movimentValid

    def peoVaEnrere(self, pasEndavant: int) -> bool:
        return (self.blanca and pasEndavant > 0) or (not self.blanca and pasEndavant < 0)

    def moure2caselles(self, tauler: Tauler) -> bool:
        if self.moguda:
            return False
        if self.blanca:
            return tauler.taulerDeJoc[2][self.posicio.columna] is None
        else:
            return tauler.taulerDeJoc[5][self.posicio.columna] is None

    def mataPecaRival(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        pecaMatada: Peca = tauler.taulerDeJoc[posicioFinal.fila][posicioFinal.columna]
        if not (pecaMatada is None):
            return True
        if self.posicio.fila == 3 or self.posicio.fila == 4:
            return self.mataPeoPassant(tauler, posicioFinal)
        return False

    def mataPeoPassant(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if self.blanca:
            peoPassant: Peca = tauler.taulerDeJoc[4][posicioFinal.columna]
            filaSortidaPassant: int = 6
        else:
            peoPassant: Peca = tauler.taulerDeJoc[3][posicioFinal.columna]
            filaSortidaPassant: int = 1
        return (tauler.ultimMoviment.pecaMoguda == peoPassant) and \
               (tauler.ultimMoviment.posicioInicial.fila == filaSortidaPassant)

    'MètodeRedefinit'
    def casellaLegal(self, tauler: Tauler, posicio: Posicio) -> bool:
        pecaArribada: Peca = tauler.taulerDeJoc[posicio.fila][posicio.columna]
        if posicio.columna == self.posicio.columna:
            return pecaArribada is None
        elif abs(self.posicio.columna - self.posicio.columna) == 1:
            if abs(self.posicio.fila - posicio.fila) == 1:
                return (pecaArribada is None) or not (pecaArribada.blanca == self.blanca)
        return False

    'MètodeRedefinit'
    def afegeixMovimentAlJoc(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]):
        if self.movimentMatantPassant(tauler, posicioFinal):
            self.afegeixMovimentBufadaAlPassant(tauler, posicioFinal, moviments)
        else:
            super().afegeixMovimentAlJoc(tauler, posicioFinal, moviments)
            if posicioFinal.fila == 0 or posicioFinal.fila == 7:
                self.escullPecaPerCoronar()
                tauler.ultimMoviment.pecaCoronada = True
                tauler.ultimMoviment.pecaMoguda = self

    def movimentMatantPassant(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if posicioFinal.columna == self.posicio.columna:
            return False
        if not (self.posicio.fila == 3 or self.posicio.fila == 4):
            return False
        return self.mataPeoPassant(tauler, posicioFinal)

    def afegeixMovimentBufadaAlPassant(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]):
        pecaMatada: Peca = tauler.taulerDeJoc[self.posicio.fila][posicioFinal.columna]
        moviment: Moviment = Moviment(self, pecaMatada, self.posicio, posicioFinal)
        if pecaMatada.pecaProtegeixDescoberta(tauler, True):
            moviment.escacs = moviment.escacs + 1
            tauler.getRei(not self.blanca).amenacat = True
        tauler.ultimMoviment = moviment
        moviments.append(moviment)

        pecaMatada.morta = True
        tauler.setPecesVives(pecaMatada)
        self.mouPecaAlTauler(tauler, posicioFinal, moviment)

    def escullPecaPerCoronar(self):
        escullPeca = input("Acabes de coronar el peó. Introdueix 's' o 'S' si vols seleccionar la nova peça."
                           "\nIntrodueix qualsevol altre caràcter si prefereixes que es generi aleatoriament")

        if escullPeca.upper() == 'S':
            escullPeca = input("Introdueix qualsevol dels caracters ['R', 'T', 'A', 'C'] segons la peça que vulguis")
        else:
            escullPeca = random.choice(['R', 'T', 'A', 'C'])
        if escullPeca == 'R':
            self: Reina = Reina(self.posicio, self.blanca, False)
        elif escullPeca == 'T':
            self: Torre = Torre(self.posicio, self.blanca, False)
        elif escullPeca == 'A':
            self: Alfil = Alfil(self.posicio, self.blanca, False)
        else:
            self: Cavall = Cavall(self.posicio, self.blanca, False)

    def escacAlRei(self, tauler: Tauler, posicioReiRival: Posicio) -> bool:
        if abs(self.posicio.columna - posicioReiRival.columna) != 1:
            return False
        if self.blanca:
            return posicioReiRival.fila == self.posicio.fila + 1
        else:
            return posicioReiRival.fila == self.posicio.fila - 1

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        movimentsPossibles: [Moviment] = []
        if self.pecaProtegeixDescoberta(tauler, True):
            return movimentsPossibles
        if self.blanca:
            endavant: int = 1
        else:
            endavant: int = -1
        for columna in range(-1, 2):
            try:
                posicio: Posicio = Posicio(self.posicio.fila + endavant, columna)
                if self.casellaLegal(tauler, posicio):
                    if self.posicio.columna == columna:
                        movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
                    elif self.mataPecaRival(tauler, posicio):
                        movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
            except IndexError:
                {}
        if not self.moguda:
            posicio: Posicio = Posicio(self.posicio.fila + (endavant * 2), self.posicio.columna)
            if tauler.esCasellaBuida(posicio) and self.moure2caselles(tauler):
                movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))

    def imprimeix(self) -> str:
        if self.blanca:
            return 'P'
        else:
            return 'p'
