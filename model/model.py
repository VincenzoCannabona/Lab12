import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.rifugi=None                      #dizionario con tutti i rifugi, lo inizializzo a vuoto
        self.connessioni=None
        self.G=nx.Graph()

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        self.G.clear()

        #prendo tutti i rifugi dato l'anno
        self.rifugi=DAO.get_rifugi_dato_anno(year)              #è un dizionario di oggetti
        print (self.rifugi)

        #prendo le connessioni tra questi rifugi che corrispondono agli archi
        self.connessioni=DAO.get_all_connessioni(self.rifugi, year)                 #dizionario di oggetti
        print (self.connessioni)

        #costruisco il grafo
        self.G.add_nodes_from(self.rifugi)
        #la funzione get_edges accetta solo una toupla di nodi del tipo (n,m,peso)
        #self.G.add_edges_from(self.connessioni)

        difficolta=0
        #aggiungo il peso
        for id1,id2 in self.connessioni:
            if self.connessioni[(id1,id2)].difficolta=="facile":
                difficolta=1
            elif self.connessioni[(id1,id2)].difficolta=="media":
                difficolta=1.5
            elif self.connessioni[(id1,id2)].difficolta=="difficile":
                difficolta=2
            self.G.add_edge(id1,id2, weight=difficolta * float(self.connessioni[(id1,id2)].distanza))               #crea un arco in cui u,v sono le chivi e peso il dizionario di attributi

        #print (self.G[1][2])
        #print(self.connessioni[(1,2)].distanza)



    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        pesi=[]
        for n,m,p in self.G.edges(data=True):
            pesi.append(self.G[n][m]['weight'])

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
            peso = d["weight"]

            if peso < soglia:
                minori += 1
            elif peso > soglia:
                maggiori += 1

        return minori, maggiori




    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo_ricorsione(self, soglia):
        #il percorso deve essere fatto solo da archi con peso > di una soglia
        #il percorso deve contenere almeno tre nodi (due archi)

        self.soluzione_cammino_minimo=[]
        self.costo_minimo_migliore=float("inf")

        #devo fare una ricerca partendo da ogni nodo
        for n in self.G.nodes():
            nodo_partenza=[n]
            archi_visitati=[]
            self.ricorsione(nodo_partenza, archi_visitati, soglia)

        return self.soluzione_cammino_minimo


    def ricorsione(self, nodo_partenza, archi_visitati, soglia ):

        if archi_visitati:               #controllo che ci siano effettivamente degli archi all'interno della soluzione
            cost=self.calcola_peso_archi(archi_visitati)

            if cost >= self.costo_minimo_migliore:
                return

            #il percorso deve contenere almeno tre nodi (due archi)
            if len(archi_visitati) >= 2:
                self.costo_minimo_migliore = cost
                self.soluzione_cammino_minimo = archi_visitati[:]  # gli devo passare una copia sennò ogni volta che la ricorsione ricomincia cambio il risultato, [:] crea una copia della lista




        #condizione per i vicini
        ultimo_nodo= nodo_partenza[-1]
        vicini= self.get_vicini_ammissibili(ultimo_nodo, nodo_partenza, soglia)

        for v in vicini:
            #aggiorno le liste da passare alla prossima ricorsione
            nodo_partenza.append(v)
            peso=self.G.get_edge_data(ultimo_nodo, v)
            archi_visitati.append((ultimo_nodo,v,peso))     #passo una tupla  cosi quando vado nella fuznione calcola peso py può spacchettarla facilmente
            self.ricorsione(nodo_partenza, archi_visitati, soglia)
            #sempre backtraking
            nodo_partenza.pop()
            archi_visitati.pop()


    def get_vicini_ammissibili(self, ultimo_nodo, nodi_parziali, soglia):
        #ultimo nodo= nodo da considerare per calcolare i vicini
        #devo evitare di ripassare sugli stessi nodi
        #ogni arco deve avere un peso > della soglia
        vicini=[]
        for v in self.G.neighbors(ultimo_nodo):
            if v in nodi_parziali:         #se il vicino è già stato visitato (sennò entrerei in un loop)
                continue                    #salta direttamente il resto del ciclo
            peso=self.G.get_edge_data(ultimo_nodo, v)               #dizionario degli attributi
            w=peso.get("weight",None)                                    #tutto compatto peso = self.G[ultimo_nodo][v].get('weight', 0.0)
            if w is None:
                continue
            if w>soglia:
                vicini.append(v)          #alla fine appendo solo il vicino che rispetta le condizioni
        return vicini


    def calcola_peso_archi(self, archi):
        totale=0.0
        for partenza,arrivo,peso in archi:
            if peso:
                totale += peso.get("weight", 0.0)       #se non trovo il peso gestisco l'errore impostando al valore di defoult 0.0

        return totale
