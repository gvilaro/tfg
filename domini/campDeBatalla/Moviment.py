from . import Posicio
from ..exercit import Peca


class Moviment:
    def __init__(self, pecaMoguda: Peca, pecaMatada: Peca, posicioInicial: Posicio, posicioFinal: Posicio,
                 pecaCoronada: bool = False, escacs: int = 0):
        self.pecaMoguda = pecaMoguda
        self.pecaMatada = pecaMatada
        self.posicioInicial = posicioInicial
        self.posicioFinal = posicioFinal
        self.pecaCoronada = pecaCoronada
        self.escacs = escacs

