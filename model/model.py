import networkx as nx
from networkx.generators.social import florentine_families_graph

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G=nx.Graph()
        self.refuges=None
        self.connessioni=None

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO

        self.G.clear()

        self.refuges=DAO.get_all_rifugi(year)

        self.connessioni=DAO.get_connessioni(self.refuges, year)

        self.G.add_nodes_from(self.refuges.keys())

        #print (self.refuges)

        difficolta_num=0
        for c in self.connessioni:
            if c.difficolta=="facile":
                difficolta_num=1
            elif c.difficolta=="medio":
                difficolta_num=1.5
            elif c.difficolta=="difficile":
                difficolta_num=2
            self.G.add_edge(c.id_rifugio1,c.id_rifugio2, peso=c.distanza*difficolta_num)

        #print(self.G)

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        pesi=[]
        for u,v,p in self.G.edges(data=True):
            peso=self.G[u][v]['peso']
            pesi.append(peso)

        return min(pesi), max(pesi)

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        minori = 0
        maggiori = 0

        for u, v, d in self.G.edges(data=True):
            peso = d["peso"]

            if peso < soglia:
                minori += 1
            elif peso > soglia:
                maggiori += 1

        return minori, maggiori

    """Implementare la parte di ricerca del cammino minimo"""

    def calcola_cammino_minimo(self, soglia):
        G_filtrato = nx.Graph()

        for u, v, d in self.G.edges(data=True):
            if d["peso"] > int(soglia):
                G_filtrato.add_edge(u, v, peso=d["peso"])

        G_filtrato.add_nodes_from(self.G.nodes())

        best_cost = float("inf")
        best_path = None

        for source in G_filtrato.nodes():
            distanze = nx.single_source_dijkstra_path_length(
                G_filtrato, source, weight="peso")

            for target, costo in distanze.items():
                if source == target:
                    continue

                path = nx.dijkstra_path(
                    G_filtrato, source, target, weight="peso")

                if len(path) >= 3 and costo < best_cost:
                    best_cost = costo
                    best_path = path

        if best_path is None:
            return []

        risultato = []
        for nodo_id in best_path:
            r = self.refuges[nodo_id]
            risultato.append((r.id, r.nome))

        return risultato

    def cammino_minimo(self, soglia):
        self.best_path = []
        self.best_weight = float("inf")

        for nodo in self.G.nodes():
            self._dfs(
                nodo_corrente=nodo,
                soglia=soglia,
                percorso=[nodo],
                peso_corrente=0
            )

        return self.best_path

    def _dfs(self, nodo_corrente, soglia, percorso, peso_corrente):
        if len(percorso) >= 3:
            if peso_corrente < self.best_weight:
                self.best_weight = peso_corrente
                self.best_path = percorso.copy()

        for vicino in self.G.neighbors(nodo_corrente):

            if vicino in percorso:
                continue

            peso_arco = self.G[nodo_corrente][vicino]["peso"]

            if peso_arco <= soglia:
                continue

            percorso.append(vicino)

            self._dfs(
                nodo_corrente=vicino,
                soglia=soglia,
                percorso=percorso,
                peso_corrente=peso_corrente + peso_arco
            )

            percorso.pop()




