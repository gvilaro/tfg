from random import random

from .campDeBatalla import Tauler, Moviment, Posicio
from .exercit.Peca import Peca
from .exercit.Rei import Rei


class Joc:
    def __init__(self):
        self.tornBlanques: bool = True
        self.tauler: Tauler = Tauler()
        self.moviments: [Moviment]
        self.movimentsPossibles: [Moviment]

    def reiAmenacat(self):
        rei: Rei = self.tauler.getRei(self.tornBlanques)
        return rei.amenacat

    def escacMat(self) -> bool:
        reiAmenacat: Rei = self.tauler.getRei(self.tornBlanques)
        return reiAmenacat.escacMat(self.tauler)

    def jugadorOfegat(self) -> bool:
        pecesRivals: [Peca] = self.tauler.getPecesVives(not self.tornBlanques)
        for peca in pecesRivals:
            if not peca.pecaOfegada(self.tauler):
                return False
        return True

    def movimentsPossibles(self) -> [Moviment]:
        moviments: [Moviment]
        pecesVivesJugadorActual: [Peca] = self.tauler.getPecesVives(self.tornBlanques)
        for peca in pecesVivesJugadorActual:
            moviments.extend(peca.movimentsPossibles(self.tauler))
        return moviments

    def obtenirMovimentAleatori(self) -> Moviment:
        pecaAleatoria: Peca = random.choice(self.tauler.getPecesVives(self.tornBlanques))
        movimentsPecaAleatoria: [Moviment] = pecaAleatoria.movimentsPossibles(self.tauler)
        while len(movimentsPecaAleatoria) == 0:
            pecaAleatoria = random.choice(self.tauler.getPecesVives(self.tornBlanques))
            movimentsPecaAleatoria = pecaAleatoria.movimentsPossibles(self.tauler)
        return random.choice(movimentsPecaAleatoria)

