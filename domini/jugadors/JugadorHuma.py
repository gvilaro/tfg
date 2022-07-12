from domini.constants.EstatsPartida import Estats
from domini.jugadors import Jugador
from ..campDeBatalla import Moviment, Posicio, Tauler
from ..exercit.Peca import Peca, Rei


class JugadorHuma(Jugador):
    def __init__(self, blanca: bool):
        super().__init__(blanca)

    def retornaMoviment(self, tauler: Tauler) -> Moviment:
        peca: Peca = None
        while peca is None or peca.blanca != self.blanca:
            posicioPeca: Posicio = self.demanaPosicio(Estats.TRIAR_PECA)
            peca = tauler.taulerDeJoc[posicioPeca.fila][posicioPeca.columna]
        posicioDesti: Posicio = None
        while posicioDesti is None:
            posicioDesti: Posicio = self.demanaPosicio(Estats.NOVA_POSICIO_PECA)
        return Moviment(peca, None, peca.posicio, posicioDesti)

    def retornaMovimentAmbReiAmenacat(self, tauler: Tauler) -> Moviment:
        if self.escacEvitable(tauler):
            rei: Rei = tauler.getRei(self.blanca)
            while True:
                moviment: Moviment = self.retornaMoviment(tauler)
                if isinstance(moviment.pecaMoguda, Rei):
                    moviments: [Moviment] = rei.movimentsPossibles(tauler)
                else:
                    moviments: [Moviment] = rei.movimentsProteccioReiAmenacat(tauler)

                for movimentPossible in moviments:
                    if movimentPossible.posicioFinal.esIgual(moviment.posicioFinal):
                        return moviment
                print(Estats.MOVIMENT_NO_LEGAL_EN_ESCAC)
        return None

    def demanaPosicio(self, missatge: str) -> Posicio:
        posicio: Posicio = None
        while posicio is None:
            posicioPeca: str = input(missatge)
            try:
                fila: int = int(posicioPeca[0])
                columna: int = int(posicioPeca[2])
                posicio: Posicio = Posicio(fila, columna)
            except Exception:
                {}
        return posicio

    def escacEvitable(self, tauler: Tauler) -> bool:
        moviments: [Moviment] = self.obtenirMovimentsPossiblesEnEscac(tauler)
        return len(moviments) > 0
