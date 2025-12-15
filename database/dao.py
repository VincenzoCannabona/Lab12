from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def get_all_rifugi(year):
        """
        Restituisce il dizionario di tutti i rifugi collegati da almeno un sentiero fino all'anno specificato.
        :param year: anno massimo da considerare
        """
        conn = DBConnect.get_connection()
        rifugi = {}

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                    FROM rifugio r, connessione c
                    WHERE c.anno <= %s and (r.id = c.id_rifugio1 or r.id = c.id_rifugio2)
                    ORDER BY r.nome
                    """
        cursor.execute(query, (year,))

        for row in cursor:
            if rifugi.get(row['id']) is None:
                rifugi[row["id"]] = Rifugio(**row)

        cursor.close()
        conn.close()
        return rifugi

    @staticmethod
    def get_connessioni(rifugi, year):
        """
        Restituisce tutte le connessioni tra rifugi fino all'anno specificato e solo di tipo principale (pathtype=1).
        :param: rifugi: dizionario {rifugio_id: Rifugio} per associare gli oggetti ai loro id.
        :param: year: anno massimo da considerare
        """
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                    SELECT id_rifugio1, id_rifugio2, distanza, difficolta, durata
                    FROM connessione
                    WHERE anno <= %s
                    """
        cursor.execute(query, (year,))

        for row in cursor:
            connessioni = Connessione(**row)
            result.append(connessioni)

        cursor.close()
        conn.close()
        return result

