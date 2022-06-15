from ..Peca import Peca
from ..Rei import Rei
from ..Reina import Reina
from ..Peo import Peo
from ..Alfil import Alfil
from ..Cavall import Cavall
from ..Torre import Torre
from...campDeBatalla.Posicio import Posicio


class FactoriaDePeces:
    @staticmethod
    def creaPeca(pecaBlanca: bool, fila: int, columna: int) -> Peca:
        if fila == 1 or fila == 6:
            return Peo(pecaBlanca, Posicio(fila, columna))
        elif columna == 0:
            return Torre(pecaBlanca, Posicio(fila, columna))
        elif columna == 1:
            return Cavall(pecaBlanca, Posicio(fila, columna))
        elif columna == 2:
            return Alfil(pecaBlanca, Posicio(fila, columna))
        elif columna == 3:
            return Reina(pecaBlanca, Posicio(fila, columna))
        elif columna == 4:
            return Rei(pecaBlanca, Posicio(fila, columna))
        elif columna == 5:
            return Alfil(pecaBlanca, Posicio(fila, columna))
        elif columna == 6:
            return Cavall(pecaBlanca, Posicio(fila, columna))
        elif columna == 7:
            return Torre(pecaBlanca, Posicio(fila, columna))
