from tkinter import Frame, Label
from assets.contantes import *
from utils.ui_utils import create_button_menu
from .notifications_view import NotificationsView
from .reservation_view import ReservationView
from .table_view import TableView


class MainWindow:
    def __init__(self, fenetre, reservation_controler, table_controller, notification_controller):
        self.fenetre = fenetre

        # Titre de la partie gauche
        self.label_titre = Label(fenetre, text="La Bonne Fourchette", font=(
            POLICE, 34, "bold"), background=DARK_CREAM_COLOR, anchor="w")
        self.label_titre.pack(pady=(10, 0), padx=(50, 0), anchor="nw")

        # Créer une frame pour la partie gauche (40% de la largeur)
        self.frame_gauche = Frame(fenetre, width=0.35 * 1920, background=LIGHT_CREAM_COLOR)
        self.frame_gauche.pack(side="left", fill="y", padx=10)
        self.frame_gauche.pack_propagate(False)  # Fixer la taille

        # Créer la frame des boutons à l'intérieur de frame_gauche
        self.frame_boutons = Frame(self.frame_gauche, background=LIGHT_CREAM_COLOR)
        self.frame_boutons.pack(pady=20, padx=20, fill="y")

        # Ligne de séparation
        self.ligne_separation = Frame(fenetre, width=5, background="white")
        self.ligne_separation.pack(side="left", fill="y")

        # Créer la zone d'affichage sur la droite (60% de la largeur)
        self.frame_droite = Frame(fenetre, width=0.50 * 1920, background=LIGHT_CREAM_COLOR)
        self.frame_droite.pack(side="left", fill="both", padx=50, expand=True)
        self.frame_droite.pack_propagate(False)  # Fixer la taille

        self.not_view = NotificationsView(notification_controller, self.frame_droite)
        self.res_view = ReservationView(table_controller, reservation_controler, self.frame_droite)
        self.tab_view = TableView(table_controller, reservation_controler,  self.frame_droite)

    def verifier_et_notifier(self):
        """Vérifie les tables et affiche des notifications si nécessaire."""
        self.not_view.not_ctrl.check_status()
        self.fenetre.after(60000, self.verifier_et_notifier)

    def run(self):

        # Utilisation de la fonction pour créer les boutons
        create_button_menu(self.frame_boutons, "Afficher les Tables", (POLICE, 18), BTN_SIZE_Y, BTN_SIZE_X, RED_COLOR,
                           lambda: self.tab_view.afficher_tables(self.tab_view.tab_ctrl.tables), 0, 0)
        create_button_menu(self.frame_boutons, "Afficher les Reservations", (POLICE, 18), BTN_SIZE_Y, BTN_SIZE_X, RED_COLOR,
                           lambda: self.res_view.afficher_reservations(self.res_view.res_ctrl.reservations), 0, 1)
        create_button_menu(self.frame_boutons, "Afficher Notifications", (POLICE, 18), BTN_SIZE_Y, BTN_SIZE_X, "lightcoral",
                           self.not_view.afficher_notifications, 1, 0)
        create_button_menu(self.frame_boutons, "Créer Une Reservation", (POLICE, 18), BTN_SIZE_Y, BTN_SIZE_X, "lightcoral",
                           self.res_view.afficher_reservations_type, 1, 1)
        self.verifier_et_notifier()