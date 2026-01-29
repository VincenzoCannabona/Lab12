import datetime
from dataclasses import dataclass

@dataclass
class Connessione:
    id: int
    id_rifugio1: int
    id_rifugio2: int
    distanza: float
    difficolta: str
    anno: int
    durata: datetime.time = datetime.time(0, 0, 0)

    def __str__(self):
        return f"{self.id_rifugio1} - {self.id_rifugio2}, distanza: {self.distanza}, difficolta: {self.difficolta}, durata: {self.durata}"


    def __repr__(self):
        return f"{self.id_rifugio1} - {self.id_rifugio2}, distanza: {self.distanza}, difficolta: {self.difficolta}, durata: {self.durata}"


    def __hash__(self):
        return hash(self.id)
