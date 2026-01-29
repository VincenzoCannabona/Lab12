from dataclasses import dataclass


@dataclass
class Rifugio:            #ctrl+a
    id: int
    nome: str
    localita: str
    altitudine: int
    capienza: int
    aperto: int


    def __str__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"


    def __repr__(self):
        return f"[{self.id}] {self.nome} ({self.localita})"


    def __lt__(self, other):
        return self.id < other.id


    def __hash__(self):
        return hash(self.id)
