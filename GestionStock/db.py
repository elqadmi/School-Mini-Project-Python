import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect('stock.db')
        c = conn.cursor()


        c.execute('''CREATE TABLE IF NOT EXISTS clients (
                           client_id INTEGER PRIMARY KEY,
                           nom TEXT,
                           adresse TEXT,
                           email TEXT,
                           telephone TEXT
                           )''')


        c.execute('''CREATE TABLE IF NOT EXISTS fournisseurs (
                           fournisseur_id INTEGER PRIMARY KEY,
                           nom TEXT,
                           adresse TEXT,
                           email TEXT,
                           telephone TEXT
                           )''')


        c.execute('''CREATE TABLE IF NOT EXISTS produits (
                               produit_id INTEGER PRIMARY KEY,
                               nom TEXT,
                               description TEXT,
                               prix_unitaire REAL,
                               quantite_stock INTEGER,
                               fournisseur_id INTEGER,
                               FOREIGN KEY (fournisseur_id) REFERENCES fournisseurs(fournisseur_id)
                               )''')


        c.execute('''CREATE TABLE IF NOT EXISTS commandes (
                           commande_id INTEGER PRIMARY KEY,
                           id_client INTEGER,
                           date_commande DATE,
                           produits TEXT,
                           montant_total REAL,
                           FOREIGN KEY (id_client) REFERENCES clients(client_id)
                           )''')

        conn.commit()
    except sqlite3.Error as e:
        print("Error creating tables:", e)

if __name__ == '__main__':
    create_tables()
