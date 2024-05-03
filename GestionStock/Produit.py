import sqlite3

class Produit:
    def __init__(self, nom, description, prix_unitaire, quantite_stock, fournisseur_id):
        self.nom = nom
        self.description = description
        self.prix_unitaire = prix_unitaire
        self.quantite_stock = quantite_stock
        self.fournisseur_id = fournisseur_id

    def add_to_database(self):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("INSERT INTO produits (nom, description, prix_unitaire, quantite_stock, fournisseur_id) VALUES (?, ?, ?, ?, ?)",
                      (self.nom, self.description, self.prix_unitaire, self.quantite_stock, self.fournisseur_id))
            conn.commit()
            conn.close()
            return "Produit ajouté avec succès à la base de données."
        except Exception as e:
            return f"Erreur lors de l'ajout du produit à la base de données : {str(e)}"

    @staticmethod
    def get_all_produits():
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("SELECT * FROM produits")
            produits = c.fetchall()
            conn.close()
            return produits
        except Exception as e:
            print(f"Erreur lors de la récupération des produits depuis la base de données : {str(e)}")
            return None

    @staticmethod
    def search_by_name(keyword):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("SELECT * FROM produits WHERE nom LIKE ?", ('%' + keyword + '%',))
            produits = c.fetchall()
            conn.close()
            return produits
        except Exception as e:
            print(f"Erreur lors de la recherche de produits par nom : {str(e)}")
            return None

    def update_in_database(self, produit_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("UPDATE produits SET nom=?, description=?, prix_unitaire=?, quantite_stock=?, fournisseur_id=? WHERE produit_id=?",
                      (self.nom, self.description, self.prix_unitaire, self.quantite_stock, self.fournisseur_id, produit_id))
            conn.commit()
            conn.close()
            return "Produit mis à jour avec succès dans la base de données."
        except Exception as e:
            return f"Erreur lors de la mise à jour du produit dans la base de données : {str(e)}"

    @staticmethod
    def delete_from_database(produit_id):
        try:
            conn = sqlite3.connect('stock.db')
            c = conn.cursor()
            c.execute("DELETE FROM produits WHERE produit_id=?", (produit_id,))
            conn.commit()
            conn.close()
            return "Produit supprimé avec succès de la base de données."
        except Exception as e:
            return f"Erreur lors de la suppression du produit de la base de données : {str(e)}"
