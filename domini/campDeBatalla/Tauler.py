from ..exercit.Peca import Peca
from ..exercit.Rei import Rei
from .Posicio import Posicio
from .Moviment import Moviment
from..exercit.factoria.FactoriaDePeces import FactoriaDePeces


class Tauler:
    def __init__(self):
        self.taulerDeJoc: [[Peca] * 8 for i in range(8)] = []
        self.pecesBlanquesVives: [Peca] = []
        self.pecesNegresVives: [Peca] = []
        self.reiBlanc: Rei = None
        self.reiNegre: Rei = None
        self.ultimMoviment: Moviment = None

    def inicialitzaTauler(self):
        self.inicialitzaExercitReiBlanc()
        for fila in range(2, 6):
            for columna in range(0, 8):
                self.taulerDeJoc[fila][columna] = None
        self.inicialitzaExercitReiNegre()

    def inicialitzaExercitReiBlanc(self):
        for fila in [0, 1]:
            for columna in range(0, 8):
                peca: Peca = FactoriaDePeces.creaPeca(True, fila, columna)
                self.taulerDeJoc[fila][columna] = peca
                self.pecesBlanquesVives.append(peca)
        self.reiBlanc = self.taulerDeJoc[0][4]

    def inicialitzaExercitReiNegre(self):
        for fila in [7, 6]:
            for columna in range(0, 8):
                peca: Peca = FactoriaDePeces.creaPeca(False, fila, columna)
                self.taulerDeJoc[fila][columna] = peca
                self.pecesNegresVives.append(peca)
        self.reiNegre = self.taulerDeJoc[7][4]

    def getPecesVives(self, blanques: bool) -> [Peca]:
        if blanques:
            return self.pecesBlanquesVives
        else:
            return self.pecesNegresVives

    def setPecesVives(self, peca: Peca):
        if peca.blanca:
            self.pecesBlanquesVives.remove(peca)
        else:
            self.pecesNegresVives.remove(peca)

    def getRei(self, blanc: bool) -> Rei:
        if blanc:
            return self.reiBlanc
        else:
            return self.reiNegre

    def setCasella(self, posicio: Posicio, peca: Peca):
        self.taulerDeJoc[posicio.fila][posicio.columna] = peca

    def esCasellaBuida(self, posicio: Posicio) -> bool:
        return self.taulerDeJoc[posicio.fila][posicio.columna] is None

    def imprimeix(self) -> str:
        dibuixTauler: str = ""
        for fila in range(0, len(self.taulerDeJoc)):
            for columna in range(0, len(self.taulerDeJoc[fila])):
                peca: Peca = self.taulerDeJoc[fila][columna]
                dibuixTauler = '{0}{1},'.format(dibuixTauler, peca.imprimeix())
            dibuixTauler = dibuixTauler[0:-1] + '\n'
        return dibuixTauler

