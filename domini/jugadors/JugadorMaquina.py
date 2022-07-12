from random import random

from ..campDeBatalla import Moviment, Tauler
from ..constants.EstatsPartida import Estats
from ..jugadors import Jugador


class JugadorMaquina(Jugador):
    def __init__(self, blanca: bool, algoritmeAI: str = Estats.MODE_ALEATORI):
        super().__init__(blanca)
        self.algoritmeAI = algoritmeAI

    def retornaMoviment(self, tauler: Tauler) -> Moviment:
        return self.obtenirMovimentAleatori(tauler)

    def retornaMovimentAmbReiAmenacat(self, tauler: Tauler) -> Moviment:
        return self.obtenirMovimentAleatoriEnEscac(tauler)

    def obtenirMovimentAleatori(self, tauler: Tauler) -> Moviment:
        moviments: [Moviment] = self.obtenirMovimentsPossibles(tauler, False)
        return random.choice(moviments)

    def obtenirMovimentAleatoriEnEscac(self, tauler) -> Moviment:
        moviments: [Moviment] = self.obtenirMovimentsPossiblesEnEscac(tauler)
        if len(moviments) == 0:
            return None
        return random.choice(moviments)
