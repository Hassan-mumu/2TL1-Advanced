from controllers.reservation_controller import ReservationController
from controllers.table_controller import TableController
from utils.formular_utils import *
from utils.ui_utils import *


class TableView:
    def __init__(self, table_controller : TableController ,reservation_controller : ReservationController, frame):
        self.tab_ctrl = table_controller
        self.res_ctrl = reservation_controller
        self.frame = frame

    def afficher_tables(self, liste_tables=None):
        """Affiche la liste des tables avec une grille et une scrollbar."""
        frame = configurer_scrollable_frame(self.frame)
        x, y = 0, 0

        Button(
            frame, text="Ajouter table", font=(POLICE, 12, "bold"),
            bg="green", fg="white", command=self.menu_creer_table
        ).grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        Button(
            frame, text="Supprimer table", font=(POLICE, 12, "bold"),
            bg="gold", fg="black", command=self.menu_creer_table
        ).grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        liste_tables = liste_tables if liste_tables else self.tab_ctrl.tables

        if not liste_tables :
            displayEmpty(frame, EMPTY_TABLE)
        else:
            for table in liste_tables :
                cadre_table = Frame(frame, background="white",pady=10,
                                    padx=10, relief="raised", borderwidth=2)
                cadre_table.grid(pady=10, padx=10, column=x, row=y + 1)

                afficher_details_table(cadre_table, table)
                cadre_table.bind("<Button-1>", lambda event, ct=cadre_table,
                                                      t=table: self.basculer_options_table(ct, t))

                if x == 3:  # 4 colonnes par ligne
                    y += 1
                x = (x + 1) % 4


    def afficher_options_table(self,cadre, table: Table):
        """Affiche les boutons Réserver et Voir Réservations dans le cadre donné."""
        Button(
            cadre, text="Réserver", font=(POLICE, 14), background="lightgreen",
            command=lambda: self.menu_reserver_table(table)
        ).pack(pady=5, padx=10, anchor="w")

        print(table.reservations)

        Button(
            cadre, text="Réservations", font=(POLICE, 14), background="lightblue",
            command=lambda: self.afficher_reservations(table.reservations)
        ).pack(pady=5, padx=10, anchor="w")

        Button(
            cadre, text="Supprimer", font=(POLICE, 14), background="gold",
            command=lambda: self.confirmer_suppression(table)
        ).pack(pady=5, padx=10, anchor="w")


    def basculer_options_table(self,cadre_table, table: Table):
        """Affiche ou masque les options d'une table dans son cadre."""
        if any(isinstance(widget, Button) for widget in cadre_table.winfo_children()):
            # Si les options sont présentes, réaffiche seulement les détails
            for widget in cadre_table.winfo_children():
                widget.destroy()
            afficher_details_table(cadre_table, table)
        else:
            # Sinon, affiche les options
            for widget in cadre_table.winfo_children():
                widget.destroy()
            afficher_details_table(cadre_table, table)
            self.afficher_options_table(cadre_table, table)


    def afficher_reservations(self, liste_reservations=None):
        """Affiche la liste des réservations avec une grille et une scrollbar."""
        frame = configurer_scrollable_frame(self.frame)
        x, y = 0, 0
        print(liste_reservations)
        liste_reservations = liste_reservations if liste_reservations is not None else self.res_ctrl.reservations
        if liste_reservations :
            displayEmpty(frame, EMPTY_RESERVATION)
        else:
            for reservation in liste_reservations:
                cadre_reservation = Frame(
                    frame, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
                cadre_reservation.grid(pady=10, padx=10, column=x, row=y)

                afficher_details_reservation(cadre_reservation, reservation)

                if x == 3:  # 4 colonnes par ligne
                    y += 1
                x = (x + 1) % 4


    def menu_reserver_table(self, table: Table):
        """Affiche un écran pour sélectionner la date, l'heure et le nom de réservation."""
        frame = configurer_scrollable_frame(self.frame)

        nom_var = ajouter_champ_nom(frame)
        frame_principal = Frame(frame, background=LIGHT_CREAM_COLOR)
        frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
        cal = ajouter_calendrier(frame_principal)
        selected_time_var = ajouter_choix_horaires(frame_principal)

        # Bouton de validation
        Button(
            frame, text="Valider", font=(POLICE, 14),
            background="lightgreen", command=lambda: self.valider_reservation_table(table, cal, selected_time_var, nom_var)
        ).pack(pady=20)


    def valider_reservation_table(self, table: Table, cal, selected_time_var, nom_var):
        """Valide la réservation et affiche une confirmation."""
        selected_date = datetime.strptime(cal.get_date(), "%m/%d/%y").date()
        selected_time = datetime.strptime(selected_time_var.get(), "%H:%M").time()
        nom_reservation = nom_var.get().strip() or "defaultName"

        reservation = self.res_ctrl.ajouter_reservation(table, selected_date, selected_time, nom_reservation)
        # noinspection PyTypeChecker

        if selected_time:
            afficher_confirmation(self.frame, reservation)
        else:
            Label(self.frame, text="Veuillez sélectionner une heure !",
                  font=(POLICE, 14), background="red").pack(pady=10)

    def valider_entree(self,entree):
        valeur = entree.get()
        try:
            valeur_int = int(valeur)
            if 2 <= valeur_int <= 8:
                self.tab_ctrl.add_table(Table(valeur_int))
                self.afficher_tables(self.tab_ctrl.tables)
            else:
                print(f"valeur invalide : {valeur} n'est pas compris entre 2 et 8")
                self.menu_creer_table()
        except ValueError:
            print(f"valeur invalide : {valeur}")

    def menu_creer_table(self):
        frame = configurer_scrollable_frame(self.frame)
        frame.pack(fill="x", pady=10)

        Label(
            frame, text="Entré nombre de place pour la table : ", font=(POLICE, 26),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        Label(frame, text="Place:", font=(POLICE, 16),
              background=LIGHT_CREAM_COLOR).pack(side="left", padx=10)

        place = StringVar()
        Entry(frame, textvariable=place, font=(
            POLICE, 16), width=20).pack(side="left", padx=10)

        Button(
            frame, text="Valider Table", font=(POLICE, 14),
            background="lightgreen",
            command=lambda : self.valider_entree(place)
        ).pack(pady=20)

    def confirmer_suppression(self, tables):
        frame = configurer_scrollable_frame(self.frame)

        tables = [tables] if isinstance(tables, Table) else tables
        print(tables)
        res_liste = self.tab_ctrl.extract_res_from_tab(tables)
        print(res_liste)

        Label(
            frame, text="Voulez vous supprimer les tables suivantes: ", font=(POLICE, 20),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        for elem in tables:
            Label(frame, text=f"Table {elem.t_id}", font=(
                POLICE, 16), background=LIGHT_CREAM_COLOR).pack(padx=10)

        Label(
            frame, text="Cela supprimera les réservations suivantes: ", font=(POLICE, 20),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=50, padx=100)

        for elem in res_liste:
            Label(frame, text=f"Reservation {elem.res_id}", font=(
                POLICE, 16), background=LIGHT_CREAM_COLOR).pack(padx=10)

        Button( frame, text="Confirmer", font=(POLICE, 14), background="lightgreen",
                command= lambda : self.afficher_suppression( tables, res_liste) ).pack(side="left", padx=20)

        Button(frame, text="Annuler", font=(POLICE, 14), background="red",
            command=self.afficher_tables).pack(side="left" ,padx=20)


    def afficher_suppression(self, tables, reservation_liste):
        frame = configurer_scrollable_frame(self.frame)
        Label(
            frame, text="les tables suivantes ont été supprimées: ", font=(POLICE, 20),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        for elem in tables:
            Label(frame, text=f"Table {elem.t_id}", font=(
                POLICE, 16), background="white").pack(anchor="w", padx=10)

        Label(
            frame, text="Les réservations suivantes ont été supprimées: ", font=(POLICE, 20),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        for elem in reservation_liste:
            Label(frame, text=f"Reservation {elem.res_id}", font=(
                POLICE, 16), background=LIGHT_CREAM_COLOR).pack(anchor="w", padx=100)

        Button(frame, text="Retour aux tables", font=(POLICE, 14), background="lightgreen",
               command=self.afficher_tables ).pack(side="left", pady=20)

        self.tab_ctrl.supress_tables(tables)