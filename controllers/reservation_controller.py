from models.reservation import Reservation
from models.table import Table


class ReservationController:
    def __init__(self, database_manager, table_controller):
        self.db_manager = database_manager
        self.table_controller = table_controller
        self.__reservations = self.db_manager.load_reservations(self.table_controller.tables)  # Charger les réservations depuis la DB

    @property
    def reservations(self):
        return self.__reservations

    def ajouter_reservation(self, table, res_date, res_hour, name="defaultName", babychairs=0, state='W'):
        # Vérifier la disponibilité des tables

        table = [table] if isinstance(table, Table) else table
        j = 0
        reservable = True
        while j < len(table) and reservable:
            i = 0
            while i < len(table[j].reservations) and reservable:
                reservable = self.is_reservable(table[j].reservations[i], (res_hour, res_date))
                i += 1
            if not reservable:
                print(f"La table {table.t_id} n'est pas disponible à cette heure.")
                return None
            j += 1

        # Créer la réservation
        reservation = Reservation(table, res_hour, res_date, name, babychairs=babychairs, state=state)
        self.reservations.append(reservation)
        for tables in reservation.table:
            tables.add_reservation(reservation)
        return reservation

    @staticmethod
    def is_reservable(res: Reservation, suggested_res):
        """
        Vérifie si une réservation peut être faite à une heure et une date suggérées.

        PRE : - res est une instance de la classe Reservation
              - suggested_res est un tuple contenant un objet datetime.time et un objet datetime.date
        POST : Retourne un booléen indiquant si la réservation est possible.
        """
        res_hour = res.res_hour
        res_date = res.res_date
        sug_hour = suggested_res[0]
        sug_date = suggested_res[1]
        return res_date != sug_date or (res_date == sug_date and abs(
            (res_hour.hour * 60 + res_hour.minute) - (sug_hour.hour * 60 + sug_hour.minute)) >= 90)

    def annuler_terminer_reservation(self, reservation, message):
        """Annule une réservation et libère la table."""
        if reservation in self.reservations:
            self.reservations.remove(reservation)
            reservation.change_state('T')
            print(message)

    def confirmer(self, reservation : Reservation, message):
        """Confirme ue réservation et les tables passe à l'état occupé"""
        if reservation in self.reservations:
            reservation.change_state('P')
            print(message)

    def filter_by_date_time(self, res_date, res_heure):
        """Filtre les tables disponibles à une date et heure données."""

        table_list = self.table_controller.tables
        cpy_list = [table for table in table_list]

        if self.reservations:
            cpy_list = []
            for table in table_list:
                i = 0
                reservable = True
                while i < len(table.reservations) and reservable:
                    reservable = self.is_reservable(table.reservations[i], (res_heure, res_date))
                    i += 1
                if reservable:
                    cpy_list.append(table)
        return cpy_list

