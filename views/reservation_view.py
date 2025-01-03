from controllers.reservation_controller import ReservationController
from utils.formular_utils import *
from utils.ui_utils import *
from views.table_view import TableView


class ReservationView:
    def __init__(self, table_view :TableView , reservation_controller : ReservationController , frame):
        self.res_ctrl = reservation_controller
        self.frame = frame
        self.selected_tables = []

    def afficher_reservations(self, liste_reservations=None):
        """Affiche la liste des réservations avec une grille et une scrollbar."""
        frame = configurer_scrollable_frame(self.frame)
        x, y = 0, 0

        liste_reservations = liste_reservations if liste_reservations else self.res_ctrl.reservations
        if not liste_reservations :
            displayEmpty(frame, EMPTY_RESERVATION)
        else:
            for reservation in liste_reservations:
                cadre_reservation = Frame(
                    frame, background="white", pady=10, padx=10, relief="raised", borderwidth=2)
                cadre_reservation.grid(pady=10, padx=10, column=x, row=y)

                afficher_details_reservation(cadre_reservation, reservation)
                cadre_reservation.bind("<Button-1>", lambda event, ct=cadre_reservation,
                                                      r=reservation: self.basculer_options_reservation(ct, r))

                if x == 1:  # 4 colonnes par ligne
                    y += 1
                x = (x + 1) % 2

    def basculer_options_reservation(self,cadre_reservation, reservation: Reservation):
        """Affiche ou masque les options d'une table dans son cadre."""
        if any(isinstance(widget, Button) for widget in cadre_reservation.winfo_children()):
            # Si les options sont présentes, réaffiche seulement les détails
            for widget in cadre_reservation.winfo_children():
                widget.destroy()
            afficher_details_reservation(cadre_reservation, reservation)
        else:
            # Sinon, affiche les options
            for widget in cadre_reservation.winfo_children():
                widget.destroy()
            afficher_details_reservation(cadre_reservation, reservation)
            self.afficher_options_reservation(cadre_reservation, reservation)

    def afficher_options_reservation(self,cadre, reservation: Reservation):
        """Affiche les boutons Réserver et Voir Réservations dans le cadre donné."""

        confirm_msg = f"La réservation {reservation.res_id} pour {reservation.name} à été confirmé."
        cancel_msg = f"Réservation {reservation.res_id} annulée."
        end_msg = f"Réservation {reservation.res_id} terminé."

        if reservation.state == WAITING:
            Button(
                cadre, text="Confirmer", font=(POLICE, 14), background="green",
                command=lambda: self.confirmer_choix_option(1, reservation, confirm_msg)
            ).pack(pady=5, padx=10, anchor="w")

            Button(
                cadre, text="Annuler", font=(POLICE, 14), background="red",
                command=lambda: self.confirmer_choix_option(2,reservation,cancel_msg )
            ).pack(pady=5, padx=10, anchor="w")
        else:
            Button(
                cadre, text="Terminer", font=(POLICE, 14), background="red",
                command=lambda: self.confirmer_choix_option(3, reservation, end_msg )
            ).pack(pady=5, padx=10, anchor="w")

    def confirmer_choix_option(self,option, reservation: Reservation, message):
        frame = configurer_scrollable_frame(self.frame)

        Label(
            frame, text=message, font=(POLICE, 20),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        if option == 1:
            self.res_ctrl.confirmer(reservation, message)
        elif option == 2 or option == 3:
            self.res_ctrl.annuler_terminer_reservation(reservation, message)



    def afficher_reservations_type(self):
        frame = configurer_scrollable_frame(self.frame)

        Label(
            frame, text="Choisissez un type de réservation : ", font=(POLICE, 26),
            background=LIGHT_CREAM_COLOR
        ).pack(pady=75, padx=100)

        button_frame = Frame(frame, background=LIGHT_CREAM_COLOR)
        button_frame.pack(pady=20)

        Button(
            button_frame, text="Sur Place", width=BTN_SIZE_X, height=BTN_SIZE_Y, font=(POLICE, 22),
            background="lightblue", command=self.filter_liste
        ).pack(padx=10, side="left")

        Button(
            button_frame, text="Sur Reservation", width=BTN_SIZE_X, height=BTN_SIZE_Y, font=(POLICE, 22),
            background="lightblue", command=self.choisir_date_heure
        ).pack(side="right")

    def choisir_date_heure(self):
        frame =  configurer_scrollable_frame(self.frame)
        frame_principal = Frame(frame, background=LIGHT_CREAM_COLOR)
        frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

        nom_var = ajouter_champ_nom(frame_principal)
        cal = ajouter_calendrier(frame_principal)
        selected_time_var = ajouter_choix_horaires(frame_principal)

        # Bouton de validation
        Button(
            frame, text="Valider", font=(POLICE, 14),
            background="lightgreen", command=lambda: self.filter_liste((cal, selected_time_var, nom_var))
        ).pack(pady=20)

    def filter_liste(self,reservation=None):

        reservation_hour = datetime.now().time()
        reservation_date = datetime.now().date()
        name = "defaultName"
        if reservation:
            reservation_hour = datetime.strptime(reservation[1].get(), "%H:%M").time()
            reservation_date = datetime.strptime(reservation[0].get_date(), "%m/%d/%y").date()
            name = reservation[2].get().strip() or name

        tables = self.res_ctrl.filter_by_date_time(reservation_date, reservation_hour)
        self.afficher_tables_selectionner(tables, reservation_hour, reservation_date, name)

    def afficher_tables_selectionner(self, liste_table, hour, date, name):
        """Affiche la liste des tables avec une grille et une scrollbar."""
        frame = configurer_scrollable_frame(self.frame)
        x, y = 0, 0

        # Bouton pour confirmer la sélection
        Button(
            frame, text="Confirmer la sélection", font=(POLICE, 12, "bold"),
            bg="green", fg="white", command=lambda: self.confirmer_selection(hour, date, name)
        ).grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        if not liste_table:
            displayEmpty(frame, EMPTY_TABLE)
        else:
            # Affichage des tables
            for table in liste_table:
                cadre_table = Frame(
                    frame, background="white", pady=10, padx=10,
                    relief="raised", borderwidth=2,
                )
                cadre_table.grid(pady=10, padx=10, column=x, row=y + 1)  # Décaler à cause du bouton

                afficher_details_table(cadre_table, table)

                # Ajouter un bouton de sélection pour chaque table
                var = IntVar()
                Checkbutton(
                    cadre_table, text="Sélectionner", variable=var, bg="white",
                    command=lambda t=table, v=var : self.mettre_a_jour_selection(t, v)
                ).pack(pady=5)

                if x == 3:  # 4 colonnes par ligne
                    y += 1
                x = (x + 1) % 4

    def confirmer_selection(self, hour, date, name):

        reservation  = self.res_ctrl.ajouter_reservation(self.selected_tables.copy(), date, hour, name)
        afficher_confirmation(self.frame, reservation)
        self.selected_tables.clear()

    def mettre_a_jour_selection(self, table, var):
        """Met à jour la liste des tables sélectionnées."""

        if var.get():
            self.selected_tables.append(table)
        else:
            self.selected_tables.remove(table)
