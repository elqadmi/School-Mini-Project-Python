import datetime
import sqlite3

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, \
    QMainWindow, QAction, QVBoxLayout, QTabWidget, QLabel, QTableWidgetItem, QTableWidget, QComboBox, QMessageBox
from GestionStock.Client import Client
from GestionStock.Commande import Commande
from GestionStock.Fournisseur import Fournisseur
from GestionStock.Produit import Produit

try:
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE stock (
                name text,
                quantity integer,
                cost integer
                ) """)
    conn.commit()
except Exception:
    print('DB exists')


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Admin Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)


    def handleLogin(self):
        if (self.textName.text() == 'admin' and
            self.textPass.text() == 'RSM'):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Incorrecte mot de passe au uername')

class Example(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = stackedExample()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)

        self.show()
class stackedExample(QWidget):
    def __init__(self):

        super(stackedExample, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Client')
        self.leftlist.insertItem(1, 'Produit')
        self.leftlist.insertItem(2, 'Commande')
        self.leftlist.insertItem(3, 'Fournisseur')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500,350, 200, 200)
        self.setWindowTitle('Gestion Stock')
        self.show()


    def stack1UI(self):
        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
        tabs = QTabWidget()

        self.tab9 = QWidget()
        self.tab10 = QWidget()

        tabs.addTab(self.tab9, 'Ajouter Client')
        tabs.addTab(self.tab10, 'List Client')

        self.tab9UI()
        self.tab10UI()

        layout.addWidget(tabs)
        self.stack1.setLayout(layout)


    def tab9UI(self):
        layout = QFormLayout()

        self.ok = QPushButton('Ajouter client', self)
        cancel = QPushButton('Annuler', self)

        self.client_name = QLineEdit()
        layout.addRow("Nom du client", self.client_name)

        self.client_email = QLineEdit()
        layout.addRow("Email", self.client_email)

        self.client_address = QLineEdit()
        layout.addRow("Adresse", self.client_address)

        self.client_phone = QLineEdit()
        layout.addRow("Téléphone", self.client_phone)

        layout.addWidget(self.ok)
        layout.addWidget(cancel)
        self.tab9.setLayout(layout)

        self.ok.clicked.connect(self.Ajouter_client_a_db)
        cancel.clicked.connect(self.Effacer_les_champs_client)


    def Ajouter_client_a_db(self):
        now = datetime.datetime.now()
        name = self.client_name.text()
        email = self.client_email.text()
        address = self.client_address.text()
        phone = self.client_phone.text()

        if name and email and address and phone:
            client = Client(name, email, address, phone)
            result = client.add_to_database()
            print(result)
        else:
            print("Veuillez remplir tous les champs.")

    def Effacer_les_champs_client(self):
        self.client_name.clear()
        self.client_email.clear()
        self.client_address.clear()
        self.client_phone.clear()

    def tab10UI(self):
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        lbl_client_id = QLabel()
        lbl_client_id.setText("Enter Client Name:")
        txt_client_id = QLineEdit()
        btn_search_client = QPushButton()
        btn_search_client.setText("Search")
        btn_search_client.clicked.connect(self.load_searched_client)
        search_layout.addWidget(lbl_client_id)
        search_layout.addWidget(txt_client_id)
        search_layout.addWidget(btn_search_client)

        self.client_table = QTableWidget()
        self.client_table.setColumnCount(5)
        self.client_table.setHorizontalHeaderLabels(['ID', 'Nom', 'Adresse', 'Email', 'Téléphone'])

        self.load_all_clients()

        btn_load_all_clients = QPushButton('Load All Clients')
        btn_load_all_clients.clicked.connect(self.load_all_clients)

        btn_delete_client = QPushButton('Delete Selected Client')
        btn_delete_client.clicked.connect(self.delete_selected_client)

        layout.addLayout(search_layout)
        layout.addWidget(self.client_table)
        layout.addWidget(btn_load_all_clients)
        layout.addWidget(btn_delete_client)

        self.tab10.setLayout(layout)

    def load_all_clients(self):
        self.client_table.setRowCount(0)
        clients = Client.get_all_clients()
        if clients:
            for row, client in enumerate(clients):
                self.client_table.insertRow(row)
                for col, data in enumerate(client):
                    item = QTableWidgetItem(str(data))
                    self.client_table.setItem(row, col, item)
        else:
            self.client_table.setRowCount(1)
            self.client_table.setItem(0, 0, QTableWidgetItem("No clients found in the database."))

    def load_searched_client(self):
        client_id = self.conf_text_client.text()
        self.client_table.setRowCount(0)
        if client_id:
            clients = Client.search_by_id(client_id)
        else:
            clients = Client.get_all_clients()

        if clients:
            for row, client in enumerate(clients):
                self.client_table.insertRow(row)
                for col, data in enumerate(client):
                    item = QTableWidgetItem(str(data))
                    self.client_table.setItem(row, col, item)
        else:
            self.client_table.setRowCount(1)
            self.client_table.setItem(0, 0, QTableWidgetItem("No clients found in the database."))

    def delete_selected_client(self):
        selected_row = self.client_table.currentRow()
        if selected_row != -1:
            client_id = self.client_table.item(selected_row, 0).text()
            confirm = QMessageBox.question(self, "Confirmation",
                                           f"Are you sure you want to delete client {client_id}?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                result = Client.delete_from_database(client_id)
                if "success" in result.lower():
                    self.load_all_clients()  # Reload the table after deletion
                    QMessageBox.information(self, "Information", result)
                else:
                    QMessageBox.warning(self, "Warning", result)
        else:
            QMessageBox.warning(self, "Warning", "Please select a client to delete.")

    def stack2UI(self):

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        tabs.addTab(self.tab1, 'Ajouter Produit')
        tabs.addTab(self.tab2, 'Modifier Produit')
        tabs.addTab(self.tab3, 'Afficher Produit')
        tabs.addTab(self.tab4, 'Supprimer Produit')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

        layout.addWidget(tabs)
        self.stack2.setLayout(layout)

    def tab1UI(self):
        layout = QFormLayout()

        self.ok_add = QPushButton('Ajouter Produit', self)
        cancel = QPushButton('Annuler', self)

        self.produit_name = QLineEdit()
        layout.addRow("Nom du produit", self.produit_name)

        self.produit_description = QLineEdit()
        layout.addRow("Description", self.produit_description)

        self.produit_prix = QLineEdit()
        layout.addRow("Prix", self.produit_prix)

        self.produit_quantity = QLineEdit()
        layout.addRow("Quantité en stock", self.produit_quantity)


        self.fournisseur_combobox = QComboBox()
        fournisseurs = Fournisseur.get_all_fournisseurs()
        for fournisseur in fournisseurs:
            self.fournisseur_combobox.addItem(fournisseur[1], fournisseur[0])

        layout.addRow("Select Fournisseur", self.fournisseur_combobox)

        layout.addWidget(self.ok_add)
        layout.addWidget(cancel)
        self.tab1.setLayout(layout)

        self.ok_add.clicked.connect(lambda: self.Ajouter_produit_a_db(self.fournisseur_combobox.currentData()))
        cancel.clicked.connect(self.clear_product_fields)

    def Ajouter_produit_a_db(self, fournisseur_id):
        name = self.produit_name.text()
        description = self.produit_description.text()
        price = self.produit_prix.text()
        quantity = self.produit_quantity.text()

        if name and description and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                product = Produit(name, description, price, quantity, fournisseur_id)
                result = product.add_to_database()
                print(result)
            except ValueError:
                print("Le prix doit être un ombre et la quantité doit être un entier")
        else:
            print("Veuillez remplir tous les champs.")

    def clear_product_fields(self):
        self.produit_name.clear()
        self.produit_description.clear()
        self.produit_prix.clear()
        self.produit_quantity.clear()

    def tab2UI(self):
        layout = QVBoxLayout()

        self.ok_modify = QPushButton('Modifier Produit', self)
        cancel_modify = QPushButton('Annuler', self)

        self.modify_produit_id = QLineEdit()
        layout.addWidget(QLabel("Produit ID:"))
        layout.addWidget(self.modify_produit_id)

        self.modify_produit_name = QLineEdit()
        layout.addWidget(QLabel("Nouveau nom du Produit:"))
        layout.addWidget(self.modify_produit_name)

        self.modify_produit_description = QLineEdit()
        layout.addWidget(QLabel("Nouveau Description:"))
        layout.addWidget(self.modify_produit_description)

        self.modify_produit_prix = QLineEdit()
        layout.addWidget(QLabel("Nouveau PriX:"))
        layout.addWidget(self.modify_produit_prix)

        self.modify_produit_quantity = QLineEdit()
        layout.addWidget(QLabel("Nouveau Quantité:"))
        layout.addWidget(self.modify_produit_quantity)

        layout.addWidget(self.ok_modify)
        layout.addWidget(cancel_modify)

        self.ok_modify.clicked.connect(self.modifier_produit_dans_db)
        cancel_modify.clicked.connect(self.clear_modify_fields)

        self.tab2.setLayout(layout)

    def modifier_produit_dans_db(self):
        produit_id = self.modify_produit_id.text()
        nom = self.modify_produit_name.text()
        description = self.modify_produit_description.text()
        prix = self.modify_produit_prix.text()
        quantite = self.modify_produit_quantity.text()

        if produit_id and nom and description and prix and quantite:
            try:
                produit_id = int(produit_id)
                prix = float(prix)
                quantite = int(quantite)
                produit = Produit(nom, description, prix, quantite, fournisseur_id=1)
                result = produit.update_in_database(produit_id)
                print(result)
            except ValueError:
                print("L'identifiant du produit doit être un entier. Le prix doit être un nombre et la quantité doit être un entier.")
        else:
            print("Veuillez remplir tous les champs.")


    def clear_modify_fields(self):
        self.modify_produit_id.clear()
        self.modify_produit_name.clear()
        self.modify_produit_description.clear()
        self.modify_produit_prix.clear()
        self.modify_produit_quantity.clear()

    def tab3UI(self):
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Entrez le nom du produit:")
        self.conf_text = QLineEdit()
        self.srb = QPushButton()
        self.srb.setText("Recherche")
        self.srb.clicked.connect(self.load_searched_products)
        search_layout.addWidget(self.lbl_conf_text)
        search_layout.addWidget(self.conf_text)
        search_layout.addWidget(self.srb)


        self.product_table = QTableWidget()
        self.product_table.setColumnCount(5)
        self.product_table.setHorizontalHeaderLabels(['ID', 'Nom', 'Description', 'Prix Unitaire', 'Quantité en Stock'])


        self.load_produits()

        self.load_all_products_button = QPushButton('Load All Products', self)
        self.load_all_products_button.clicked.connect(self.load_produits)

        layout.addLayout(search_layout)
        layout.addWidget(self.product_table)
        layout.addWidget(self.load_all_products_button)

        self.tab3.setLayout(layout)

    def load_searched_products(self):
        keyword = self.conf_text.text()
        self.product_table.setRowCount(0)
        if keyword:
            produits = Produit.search_by_name(keyword)
        else:
            produits = Produit.get_all_produits()

        if produits:
            for row, produit in enumerate(produits):
                self.product_table.insertRow(row)
                for col, data in enumerate(produit):
                    item = QTableWidgetItem(str(data))
                    self.product_table.setItem(row, col, item)
        else:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("Aucun produit trouvé dans la base de données."))

    def load_produits(self):
        self.product_table.setRowCount(0)
        produits = Produit.get_all_produits()
        if produits:
            for row, produit in enumerate(produits):
                self.product_table.insertRow(row)
                for col, data in enumerate(produit):
                    item = QTableWidgetItem(str(data))
                    self.product_table.setItem(row, col, item)
        else:
            self.product_table.setRowCount(1)
            self.product_table.setItem(0, 0, QTableWidgetItem("Aucun produit trouvé"))


    def tab4UI(self):
        layout = QFormLayout()
        self.ok_delete = QPushButton('Supprimer Produit', self)
        cancel = QPushButton('Annuler', self)

        self.produit_id_delete = QLineEdit()
        layout.addRow("Produit ID", self.produit_id_delete)

        layout.addWidget(self.ok_delete)
        layout.addWidget(cancel)
        self.tab4.setLayout(layout)

        self.ok_delete.clicked.connect(self.delete_produit_from_db)
        cancel.clicked.connect(self.clear_delete_fields)

    def delete_produit_from_db(self):
        produit_id = self.produit_id_delete.text()
        if produit_id:
            try:
                result = Produit.delete_from_database(produit_id)
                print(result)
            except Exception as e:
                print(f"Erreur lors de la suppression du produit: {str(e)}")
        else:
            print("Veuillez entrer un identifiant de produit.")

    def clear_delete_fields(self):
        self.produit_id_delete.clear()

    def stack3UI(self):
        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
        tabs = QTabWidget()

        self.tab5 = QWidget()
        self.tab6 = QWidget()

        tabs.addTab(self.tab5, 'Ajouter Commande')
        tabs.addTab(self.tab6, 'Afficher Commande')

        self.tab5UI()
        self.tab6UI()

        layout.addWidget(tabs)
        self.stack3.setLayout(layout)

    def tab5UI(self):
        layout = QFormLayout()

        self.ok_commande = QPushButton('Ajouter Commande', self)
        cancel_commande = QPushButton('Annuler', self)

        self.commande_client_id = QLineEdit()
        layout.addRow("Client ID", self.commande_client_id)

        self.commande_date = QLineEdit()
        layout.addRow("Date", self.commande_date)

        self.commande_products = QLineEdit()
        layout.addRow("Produits", self.commande_products)

        self.commande_total_amount = QLineEdit()
        layout.addRow("Montant Total", self.commande_total_amount)

        layout.addWidget(self.ok_commande)
        layout.addWidget(cancel_commande)
        self.tab5.setLayout(layout)

        self.ok_commande.clicked.connect(self.add_commande_to_db)
        cancel_commande.clicked.connect(self.clear_commande_fields)

    def add_commande_to_db(self):
        client_id = self.commande_client_id.text()
        date = self.commande_date.text()
        products = self.commande_products.text()
        total_amount = self.commande_total_amount.text()

        if client_id and date and products and total_amount:
            try:
                client_id = int(client_id)
                total_amount = float(total_amount)
                commande = Commande(client_id, date, products, total_amount)
                result = commande.add_to_database()
                print(result)
            except ValueError:
                print("L'identifiant du client doit être un entier et le montant total doit être un nombre.")
        else:
            print("Veuillez remplir tous les champs.")

    def tab6UI(self):
        layout = QVBoxLayout()


        search_layout = QHBoxLayout()
        self.lbl_conf_text_commande = QLabel()
        self.lbl_conf_text_commande.setText("Enter Commande ID:")
        self.conf_text_commande = QLineEdit()
        self.srb_commande = QPushButton()
        self.srb_commande.setText("Search")
        self.srb_commande.clicked.connect(self.load_searched_commandes)
        search_layout.addWidget(self.lbl_conf_text_commande)
        search_layout.addWidget(self.conf_text_commande)
        search_layout.addWidget(self.srb_commande)


        self.commande_table = QTableWidget()
        self.commande_table.setColumnCount(4)
        self.commande_table.setHorizontalHeaderLabels(['ID', 'Client ID', 'Date', 'Total Amount'])


        self.load_all_commandes()

        self.load_all_commandes_button = QPushButton('Charger Toutes Les Commandes', self)
        self.load_all_commandes_button.clicked.connect(self.load_all_commandes)

        layout.addLayout(search_layout)
        layout.addWidget(self.commande_table)
        layout.addWidget(self.load_all_commandes_button)

        self.tab6.setLayout(layout)

    def load_all_commandes(self):
        self.commande_table.setRowCount(0)
        commandes = Commande.get_all_commandes()
        if commandes:
            for row, commande in enumerate(commandes):
                self.commande_table.insertRow(row)
                for col, data in enumerate(commande):
                    item = QTableWidgetItem(str(data))
                    self.commande_table.setItem(row, col, item)
        else:
            self.commande_table.setRowCount(1)
            self.commande_table.setItem(0, 0, QTableWidgetItem("Aucune commande trouvée"))

    def load_searched_commandes(self):
        commande_id = self.conf_text_commande.text()
        self.commande_table.setRowCount(0)
        if commande_id:
            commandes = Commande.search_by_id(commande_id)
        else:
            commandes = Commande.get_all_commandes()

        if commandes:
            for row, commande in enumerate(commandes):
                self.commande_table.insertRow(row)
                for col, data in enumerate(commande):
                    item = QTableWidgetItem(str(data))
                    self.commande_table.setItem(row, col, item)
        else:
            self.commande_table.setRowCount(1)
            self.commande_table.setItem(0, 0, QTableWidgetItem("Aucune commande trouvée dans la base de données."))

    def clear_commande_fields(self):
        self.commande_client_id.clear()
        self.command


    def stack4UI(self):
        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
        tabs = QTabWidget()

        self.tab7 = QWidget()
        self.tab8 = QWidget()

        tabs.addTab(self.tab7, 'Ajouter Fournisseur')
        tabs.addTab(self.tab8, 'List Fornisseur')

        self.tab7UI()
        self.tab8UI()

        layout.addWidget(tabs)
        self.stack4.setLayout(layout)

    def tab7UI(self):
        layout = QFormLayout()

        self.ok_fournisseur = QPushButton('Ajouter Fournisseur', self)
        cancel_fournisseur = QPushButton('Annuler', self)

        self.fournisseur_nom = QLineEdit()
        layout.addRow("Nom", self.fournisseur_nom)

        self.fournisseur_adresse = QLineEdit()
        layout.addRow("Adresse", self.fournisseur_adresse)

        self.fournisseur_email = QLineEdit()
        layout.addRow("Email", self.fournisseur_email)

        self.fournisseur_telephone = QLineEdit()
        layout.addRow("Téléphone", self.fournisseur_telephone)

        layout.addWidget(self.ok_fournisseur)
        layout.addWidget(cancel_fournisseur)
        self.tab7.setLayout(layout)

        self.ok_fournisseur.clicked.connect(self.add_fournisseur_to_db)
        cancel_fournisseur.clicked.connect(self.clear_fournisseur_fields)


    def add_fournisseur_to_db(self):
        nom = self.fournisseur_nom.text()
        adresse = self.fournisseur_adresse.text()
        email = self.fournisseur_email.text()
        telephone = self.fournisseur_telephone.text()

        if nom and adresse and email and telephone:
            fournisseur = Fournisseur(nom, adresse, email, telephone)
            result = fournisseur.add_to_database()
            print(result)
        else:
            print("Veuillez remplir tous les champs.")

    def clear_fournisseur_fields(self):
        self.fournisseur_nom.clear()
        self.fournisseur_adresse.clear()
        self.fournisseur_email.clear()
        self.fournisseur_telephone.clear()

    def tab8UI(self):
        layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        lbl_fournisseur_id = QLabel()
        lbl_fournisseur_id.setText("Enter Fournisseur ID:")
        txt_fournisseur_id = QLineEdit()
        btn_search_fournisseur = QPushButton()
        btn_search_fournisseur.setText("Recherche")
        btn_search_fournisseur.clicked.connect(self.load_searched_fournisseur)
        search_layout.addWidget(lbl_fournisseur_id)
        search_layout.addWidget(txt_fournisseur_id)
        search_layout.addWidget(btn_search_fournisseur)


        self.fournisseur_table = QTableWidget()
        self.fournisseur_table.setColumnCount(5)
        self.fournisseur_table.setHorizontalHeaderLabels(['ID', 'Nom', 'Adresse', 'Email', 'Téléphone'])


        self.load_all_fournisseurs()

        btn_load_all_fournisseurs = QPushButton('Charger Tous Les Fournisseurs')
        btn_load_all_fournisseurs.clicked.connect(self.load_all_fournisseurs)


        btn_delete_fournisseur = QPushButton('Supprimer Fournisseur Seectionne')
        btn_delete_fournisseur.clicked.connect(self.delete_selected_fournisseur)

        layout.addLayout(search_layout)
        layout.addWidget(self.fournisseur_table)
        layout.addWidget(btn_load_all_fournisseurs)
        layout.addWidget(btn_delete_fournisseur)

        self.tab8.setLayout(layout)

    def load_all_fournisseurs(self):
        self.fournisseur_table.setRowCount(0)
        fournisseurs = Fournisseur.get_all_fournisseurs()
        if fournisseurs:
            for row, fournisseur in enumerate(fournisseurs):
                self.fournisseur_table.insertRow(row)
                for col, data in enumerate(fournisseur):
                    item = QTableWidgetItem(str(data))
                    self.fournisseur_table.setItem(row, col, item)
        else:
            self.fournisseur_table.setRowCount(1)
            self.fournisseur_table.setItem(0, 0, QTableWidgetItem("Aucun fournisseur trouvé dans la base de données."))

    def load_searched_fournisseur(self):
        fournisseur_id = self.conf_text_fournisseur.text()
        self.fournisseur_table.setRowCount(0)
        if fournisseur_id:
            fournisseurs = Fournisseur.search_by_id(fournisseur_id)
        else:
            fournisseurs = Fournisseur.get_all_fournisseurs()

        if fournisseurs:
            for row, fournisseur in enumerate(fournisseurs):
                self.fournisseur_table.insertRow(row)
                for col, data in enumerate(fournisseur):
                    item = QTableWidgetItem(str(data))
                    self.fournisseur_table.setItem(row, col, item)
        else:
            self.fournisseur_table.setRowCount(1)
            self.fournisseur_table.setItem(0, 0, QTableWidgetItem("Aucun fournisseur trouvé dans la base de données."))

    def delete_selected_fournisseur(self):
        selected_row = self.fournisseur_table.currentRow()
        if selected_row != -1:
            fournisseur_id = self.fournisseur_table.item(selected_row, 0).text()
            confirm = QMessageBox.question(self, "Confirmation",
                                           f"Voulez-vous vraiment supprimer le fournisseur {fournisseur_id} ?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                result = Fournisseur.delete_from_database(fournisseur_id)
                if "succès" in result.lower():
                    self.load_all_fournisseurs()  # Reload the table after deletion
                    QMessageBox.information(self, "Information", result)
                else:
                    QMessageBox.warning(self, "Avertissement", result)
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner un fournisseur à supprimer.")




    def load_products(self):
        self.product_list.clear()
        produits = Produit.get_all_produits()
        if produits:
            for produit in produits:
                self.product_list.addItem(
                    f"ID: {produit[0]}, Nom: {produit[1]}, Description: {produit[2]}, Prix Unitaire: {produit[3]}, Quantité en Stock: {produit[4]}")
        else:
            self.product_list.addItem("Aucun produit trouvé dans la base de données.")


    def display(self, i):
        self.Stack.setCurrentIndex(i)



if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Example()
        sys.exit(app.exec_())