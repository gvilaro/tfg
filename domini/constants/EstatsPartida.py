
class Estats:
    JUGANT: str = "PARTIDA EN CURS"
    OFEGAT: str = "REI OFEGAT. LA PARTIDA HA ACABAT EN TAULES"
    GUANYA_BLANC: str = "BLANQUES GUANYEN"
    GUANYA_NEGRE: str = "NEGRES GUANYEN"
    ABANDONA_BLANC: str = "ABANDONAMENT. NEGRES GUANYEN"
    ABANDONA_NEGRE: str = "ABANDONAMENT. BLANQUES GUANYEN"
    TAULES: str = "TAULES"
    RESULTAT: str
    MISSATGE_CORONAR: str = "Acabes de coronar el peó. Introdueix 's' o 'S' si vols seleccionar la nova peça." \
                            "\nIntrodueix qualsevol altre caràcter si prefereixes que es generi aleatoriament"
    TRIAR_PECA: str = "Escriu número de fila i columna separats per una coma (fila,columna) de la peça que vols moure"
    NOVA_POSICIO_PECA: str = "Escriu número de fila i columna separats per una coma (fila,columna) de la posició on " \
                             "vols moure la peça "
    MOVIMENT_NO_LEGAL: str = "Aquest moviment no és legal. Escull moviment de nou"
    MOVIMENT_NO_LEGAL_EN_ESCAC: str = "Rei amenaçat. El moviment no és legal. Escull moviment de nou"
    TRIA_COLOR_PARTIDA: str = "Vols jugar amb blanques o negres? Escriu 'B' per triar blanques o 'N' per triar negres"
    TRIA_DIFICULTAT_PARTIDA: str = "Tria el nivell de dificultat de la partida. Escriu 'B' per nivell baix o 'A' per nivell alt"
    VALOR_INCORRECTE: str = "El valor introduit és incorrecte"
    MODE_ALEATORI: str = "aleatori"
    MODE_STOCKFISH: str = "stockfish"

    def __init__(self):
        pass

    @staticmethod
    def resultatFinal(self):
        print(self.RESULTAT)
