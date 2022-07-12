from domini.campDeBatalla import Moviment
from domini.campDeBatalla import Posicio
from domini.campDeBatalla import Tauler
from domini.constants.EstatsPartida import Estats
from domini.exercit import Peca
from domini.exercit import Rei
from domini.jugadors import Jugador
from domini.jugadors import JugadorHuma
from domini.jugadors import JugadorMaquina


class Joc:
    def __init__(self):
        self.tornBlanques: bool = False
        self.tauler: Tauler = Tauler()
        self.maquina: Jugador = JugadorMaquina(False)
        self.persona: Jugador = JugadorHuma(True)
        self.jugadorActual: Jugador
        self.moviments: [Moviment] = []
        self.estatPartida: str = Estats.JUGANT

    def main(self):
        self.configuraParametresPartida()
        self.tauler.inicialitzaTauler()
        self.jugarPartida()
        Estats.resultatFinal()

    def jugarPartida(self):
        while self.estatPartida == Estats.JUGANT:
            self.actualitzaJugador()
            if self.reiAmenacat():
                self.movimentAmbReiAmenacat()
            elif self.jugadorOfegat():
                self.estatPartida = Estats.OFEGAT
            else:
                self.movimentSenseAmenaca()
            self.tauler.imprimeix()
        Estats.RESULTAT = self.estatPartida

    def reiAmenacat(self) -> bool:
        rei: Rei = self.tauler.getRei(self.tornBlanques)
        return rei.amenacat

    def actualitzaJugador(self):
        self.tornBlanques = not self.tornBlanques
        if self.maquina.blanca == self.tornBlanques:
            self.jugadorActual = self.maquina
        else:
            self.jugadorActual = self.persona

    def movimentAmbReiAmenacat(self):
        moviment: Moviment = self.jugadorActual.retornaMovimentAmbReiAmenacat(self.tauler)
        if moviment is None:
            self.declaraGuanyador(not self.tornBlanques)
        else:
            movimentLegal: bool = self.realitzaMovimentActual(moviment)
            while not movimentLegal:
                print(Estats.MOVIMENT_NO_LEGAL)
                moviment = self.jugadorActual.retornaMovimentAmbReiAmenacat(self.tauler)
                movimentLegal = self.realitzaMovimentActual(moviment)
            self.tauler.getRei(self.tornBlanques).amenacat = False

    def movimentSenseAmenaca(self):
        moviment: Moviment = self.jugadorActual.retornaMoviment(self.tauler)
        movimentLegal: bool = self.realitzaMovimentActual(moviment)
        while not movimentLegal:
            print(Estats.MOVIMENT_NO_LEGAL)
            moviment = self.jugadorActual.retornaMoviment(self.tauler)
            movimentLegal = self.realitzaMovimentActual(moviment)

    def realitzaMovimentActual(self, moviment: Moviment) -> bool:
        peca: Peca = moviment.pecaMoguda
        posicioFinal: Posicio = moviment.posicioFinal
        return peca.moure(self.tauler, posicioFinal, self.moviments)

    def jugadorOfegat(self) -> bool:
        pecesVives: [Peca] = self.tauler.getPecesVives(self.tornBlanques)
        for peca in pecesVives:
            if not peca.pecaOfegada(self.tauler):
                return False
        return True

    def configuraParametresPartida(self):
        colorJugadorPersona: str = self.demanaValorPartida(Estats.TRIA_COLOR_PARTIDA, "B,N")
        if colorJugadorPersona == "B":
            self.persona.blanca = True
            self.maquina.blanca = False
        else:
            self.persona.blanca = False
            self.maquina.blanca = True

        dificultatPartida: str = self.demanaValorPartida(Estats.TRIA_DIFICULTAT_PARTIDA, "B,A")
        if dificultatPartida == "A":
            self.maquina.algoritmeAI = Estats.MODE_STOCKFISH

    def demanaValorPartida(self, missatge: str, valorPossible: str) -> str:
        valor: str = input(missatge).upper()
        while not (valor == valorPossible[0] or valor == valorPossible[2]):
            print(Estats.VALOR_INCORRECTE)
            valor = input(missatge).upper()
        return valor

    def declaraGuanyador(self, colorGuanyador: bool):
        if colorGuanyador:
            self.estatPartida = Estats.GUANYA_BLANC
        else:
            self.estatPartida = Estats.GUANYA_NEGRE

    if __name__ == "__main__":
        main()



