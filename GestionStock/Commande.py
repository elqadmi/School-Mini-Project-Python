import sqlite3

class Commande:
    def __init__(self, id_client, date_commande, produits, montant_total):
        self.id_client = id_client
        self.date_commande = date_commande
        self.produits = produits
        self.montant_total = montant_total

    def add_to_database(self):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("INSERT INTO commandes (id_client, date_commande, produits, montant_total) VALUES (?, ?, ?, ?)",
                      (self.id_client, self.date_commande, self.produits, self.montant_total))
            conn.commit()
            conn.close()
            return "Commande ajoutée avec succès à la base de données."
        except Exception as e:
            return f"Erreur lors de l'ajout de la commande à la base de données : {str(e)}"

    @staticmethod
    def get_all_commandes():
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("SELECT * FROM commandes")
            commandes = c.fetchall()
            conn.close()
            return commandes
        except Exception as e:
            print(f"Erreur lors de la récupération des commandes depuis la base de données : {str(e)}")
            return None

    def update_in_database(self, commande_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("UPDATE commandes SET id_client=?, date_commande=?, produits=?, montant_total=? WHERE id=?",
                      (self.id_client, self.date_commande, self.produits, self.montant_total, commande_id))
            conn.commit()
            conn.close()
            return "Commande mise à jour avec succès dans la base de données."
        except Exception as e:
            return f"Erreur lors de la mise à jour de la commande dans la base de données : {str(e)}"

    @staticmethod
    def delete_from_database(commande_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("DELETE FROM commandes WHERE id=?", (commande_id,))
            conn.commit()
            conn.close()
            return "Commande supprimée avec succès de la base de données."
        except Exception as e:
            return f"Erreur lors de la suppression de la commande de la base de données : {str(e)}"
