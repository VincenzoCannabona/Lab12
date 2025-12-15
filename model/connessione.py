from dataclasses import dataclass
import datetime
from model.rifugio import Rifugio

@dataclass
class Connessione:
    id_rifugio1: Rifugio
    id_rifugio2: Rifugio
    distanza: float
    difficolta: str
    durata: datetime.time = datetime.time(0, 0, 0)


    def __str__(self):
        return (f"Connessione: {self.r1.nome} - {self.r2.nome}, "
                f"distanza: {self.distanza} km, difficoltà: {self.difficolta}, "
                f"tempo: {self.durata}")

    def __repr__(self):
        return (f"Connessione: {self.r1.nome} - {self.r2.nome}, "
                f"distanza: {self.distanza} km, difficoltà: {self.difficolta}, "
                f"tempo: {self.durata}")