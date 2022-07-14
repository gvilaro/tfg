from __future__ import annotations

import Peca
import Rei
import Reina
import Peo
import Alfil
import Cavall
import Torre
import Posicio

class FactoriaDePeces:
    @staticmethod
    def creaPeca(pecaBlanca: bool, fila: int, columna: int) -> Peca.Peca:
        if fila == 1 or fila == 6:
            return Peo.Peo(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 0:
            return Torre.Torre(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 1:
            return Cavall.Cavall(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 2:
            return Alfil.Alfil(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 3:
            return Reina.Reina(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 4:
            return Rei.Rei(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 5:
            return Alfil.Alfil(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 6:
            return Cavall.Cavall(pecaBlanca, Posicio.Posicio(fila, columna))
        elif columna == 7:
            return Torre.Torre(pecaBlanca, Posicio.Posicio(fila, columna))

