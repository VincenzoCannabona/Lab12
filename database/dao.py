from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO

    @staticmethod
    def get_rifugi_dato_anno(anno):
        cnx = DBConnect.get_connection()
        rifugi = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto 
                    FROM rifugio r, connessione c 
                    WHERE anno <= %s and (r.id = c.id_rifugio1 or  r.id = c.id_rifugio2)"""
        try:
            cursor.execute(query, (anno,))
            for row in cursor:
                if rifugi.get(row["id"]) is None:
                    rifugi[row['id']] = Rifugio(**row)         #rifugi e row sono dizionari, l'= lo trasforma in un dizionario di oggetti che ha come chiave row di id

        except Exception as e:
            print(f"Errore durante la query get_rifugi_dato_anno: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return rifugi


    @staticmethod
    def get_all_connessioni(rifugi,anno):
        cnx = DBConnect.get_connection()
        result = {}

        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT *
                    FROM connessione
                    WHERE anno <= %s """
        try:
            cursor.execute(query, (anno,))

            #passo la lista di nodi
            #per ogni nodo aggiungo la connessione se non è gia presente id_nodo-->connessione

            for row in cursor:
                r1=row["id_rifugio1"]
                r2=row["id_rifugio2"]

                if (r1,r2) not in result:
                    result[(r1,r2)] = Connessione(**row)            #la tupla di id corrisponde all'oggetto connessione

        except Exception as e:
            print(f"Errore durante la query get_all_connessioni: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

