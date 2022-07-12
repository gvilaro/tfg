from random import random

from . import Peca, Rei, Reina, Torre, Alfil, Cavall
from ..campDeBatalla import Tauler, Posicio, Moviment
from ..constants.EstatsPartida import Estats


class Peo(Peca):
    def __init__(self, blanca: bool, posicio: Posicio, morta: bool = False):
        super().__init__(blanca, posicio, morta)
        self.moguda = False
        if self.blanca:
            self.endavant = 1
        else:
            self.endavant = -1

    'sobrecàrrega Redefinit'
    def pecaProtegeixDescoberta(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        if super().pecaProtegeixDescoberta(tauler, True):
            rei: Rei = tauler.getRei(self.blanca)
            return not rei.casellaEnLinea(posicioFinal)
        return False

    def moure(self, tauler: Tauler, posicioFinal: Posicio, moviments: [Moviment]) -> bool:
        if not self.casellaLegal(tauler, posicioFinal):
            return False

        pasEndavant: int = self.posicio.fila - posicioFinal.fila
        if self.peoVaEnrere(pasEndavant) or self.pecaProtegeixDescoberta(tauler, posicioFinal):
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
        filaSortidaPassant: int = self.posicio.fila + (self.endavant * 2)
        if filaSortidaPassant == 1 or filaSortidaPassant == 6:
            return self.mataPeoPassant(tauler, posicioFinal)
        return False

    def mataPeoPassant(self, tauler: Tauler, posicioFinal: Posicio) -> bool:
        peoPassant: Peca = tauler.taulerDeJoc[self.posicio.fila][posicioFinal.columna]
        filaSortidaPassant: int = self.posicio.fila + (self.endavant * 2)
        if isinstance(peoPassant, Peo):
            return (tauler.ultimMoviment.pecaMoguda == peoPassant) and \
                   (tauler.ultimMoviment.posicioInicial.fila == filaSortidaPassant)
        return False

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
        filaSortidaPassant: int = self.posicio.fila + (self.endavant * 2)
        if filaSortidaPassant == 1 or filaSortidaPassant == 6:
            return self.mataPeoPassant(tauler, posicioFinal)
        return False

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
        escullPeca = input(Estats.MISSATGE_CORONAR)

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
        return posicioReiRival.fila == self.posicio.fila + self.endavant

    def pecaOfegada(self, tauler: Tauler) -> bool:
        return len(self.movimentsPossibles(tauler)) == 0

    def movimentsPossibles(self, tauler: Tauler) -> [Moviment]:
        movimentsPossibles: [Moviment] = []
        for fila in range(1, 3):
            for columna in range(-1, 2):
                try:
                    posicio: Posicio = Posicio(self.posicio.fila + (self.endavant * fila), columna)
                    if self.casellaLegal(tauler, posicio) and not self.pecaProtegeixDescoberta(tauler, posicio):
                        if self.posicio.columna == columna:
                            if fila == 1:
                                movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
                            elif tauler.esCasellaBuida(posicio) and self.moure2caselles(tauler):
                                movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
                        elif self.mataPecaRival(tauler, posicio):
                            movimentsPossibles.append(Moviment(self, None, self.posicio, posicio))
                except IndexError:
                    {}
        return movimentsPossibles

    def imprimeix(self) -> str:
        if self.blanca:
            return 'P'
        else:
            return 'p'
