import abc

from ..campDeBatalla import Moviment, Tauler
from ..exercit import Rei


class Jugador(metaclass=abc.ABCMeta):
    def __init__(self, blanca: bool):
        self.blanca = blanca

    @abc.abstractmethod
    def retornaMoviment(self, tauler: Tauler) -> Moviment:
        pass

    @abc.abstractmethod
    def retornaMovimentAmbReiAmenacat(self, tauler: Tauler) -> Moviment:
        pass

    def obtenirMovimentsPossiblesEnEscac(self, tauler: Tauler) -> [Moviment]:
        rei: Rei = tauler.getRei(self.blanca)
        moviments: [Moviment] = rei.movimentsPossibles(tauler)
        if tauler.ultimMoviment.escacs > 1:
            return moviments
        movimentsProteccioRei: [Moviment] = rei.movimentsProteccioReiAmenacat(tauler)
        movimentsPossibles: [Moviment] = self.obtenirMovimentsPossibles(tauler, True)
        for moviment in movimentsPossibles:
            for movimentProteccio in movimentsProteccioRei:
                if moviment.posicioFinal.esIgual(movimentProteccio.posicioFinal):
                    moviments.append(moviment)
        return moviments

    def obtenirMovimentsPossibles(self, tauler: Tauler, reiAmenacat: bool) -> [Moviment]:
        moviments: [Moviment] = []
        if reiAmenacat:
            for peca in tauler.getPecesVives(self.blanca):
                if not (isinstance(peca, Rei)):
                    moviments.extend(peca.movimentsPossibles(tauler))
        else:
            for peca in tauler.getPecesVives(self.blanca):
                moviments.extend(peca.movimentsPossibles(tauler))
        return moviments
