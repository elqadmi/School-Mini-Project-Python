import sqlite3


class Client:
    def __init__(self, nom, adresse, email, telephone):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.telephone = telephone

    def add_to_database(self):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("INSERT INTO clients (nom, adresse, email, telephone) VALUES (?, ?, ?, ?)",
                      (self.nom, self.adresse, self.email, self.telephone))
            conn.commit()
            conn.close()
            return "Client ajouté avec succès à la base de données."
        except Exception as e:
            return f"Erreur lors de l'ajout du client à la base de données : {str(e)}"

    @staticmethod
    def get_all_clients():
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("SELECT * FROM clients")
            clients = c.fetchall()
            conn.close()
            return clients
        except Exception as e:
            print(f"Erreur lors de la récupération des clients depuis la base de données : {str(e)}")
            return None

    def update_in_database(self, client_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("UPDATE clients SET nom=?, adresse=?, email=?, telephone=? WHERE id=?",
                      (self.nom, self.adresse, self.email, self.telephone, client_id))
            conn.commit()
            conn.close()
            return "Client mis à jour avec succès dans la base de données."
        except Exception as e:
            return f"Erreur lors de la mise à jour du client dans la base de données : {str(e)}"

    @staticmethod
    def delete_from_database(client_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("DELETE FROM clients WHERE client_id=?", (client_id,))
            conn.commit()
            conn.close()
            return "Client supprimé avec succès de la base de données."
        except Exception as e:
            return f"Erreur lors de la suppression du client de la base de données : {str(e)}"
