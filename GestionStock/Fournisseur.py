import sqlite3

class Fournisseur:
    def __init__(self, nom, adresse, email, telephone):
        self.nom = nom
        self.adresse = adresse
        self.email = email
        self.telephone = telephone

    def add_to_database(self):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("INSERT INTO fournisseurs (nom, adresse, email, telephone) VALUES (?, ?, ?, ?)",
                      (self.nom, self.adresse, self.email, self.telephone))
            conn.commit()
            conn.close()
            return "Fournisseur ajouté avec succès à la base de données."
        except Exception as e:
            return f"Erreur lors de l'ajout du fournisseur à la base de données : {str(e)}"

    @staticmethod
    def get_all_fournisseurs():
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("SELECT * FROM fournisseurs")
            fournisseurs = c.fetchall()
            conn.close()
            return fournisseurs
        except Exception as e:
            print(f"Erreur lors de la récupération des fournisseurs depuis la base de données : {str(e)}")
            return None

    def update_in_database(self, fournisseur_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("UPDATE fournisseurs SET nom=?, adresse=?, email=?, telephone=? WHERE id=?",
                      (self.nom, self.adresse, self.email, self.telephone, fournisseur_id))
            conn.commit()
            conn.close()
            return "Fournisseur mis à jour avec succès dans la base de données."
        except Exception as e:
            return f"Erreur lors de la mise à jour du fournisseur dans la base de données : {str(e)}"

    @staticmethod
    def delete_from_database(fournisseur_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("DELETE FROM fournisseurs WHERE fournisseur_id=?", (fournisseur_id,))
            conn.commit()
            conn.close()
            return "Fournisseur supprimé avec succès de la base de données."
        except Exception as e:
            return f"Erreur lors de la suppression du fournisseur de la base de données : {str(e)}"
