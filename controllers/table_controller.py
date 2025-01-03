# controllers/table_controller.py
from models.database_manager import DatabaseManager
from models.table import Table


class TableController:
    def __init__(self, database_manager=None):
        self.db_manager = database_manager if database_manager else DatabaseManager()
        self.__tables = self.db_manager.load_tables()  # Charger les tables depuis la DB

        if not self.tables:
            for i in range(1, 21):
                if i <= 10:
                    self.add_table(Table(2))
                elif i <= 16:
                    self.add_table(Table(4))
                else:
                    self.add_table(Table(6))

    @property
    def tables(self):
        return self.__tables

    def add_table(self, table):
        self.tables.append(table)
    
    @staticmethod
    def verifier_disponibilite(table : Table, res_hour, res_date):
        """Vérifie si la table est disponible à la date et l'heure spécifiées."""
        if table.state == 'V':  # Table libre
            return True
        elif table.state == 'R':  # Table réservée, vérifier les réservations existantes
            for reservation in table.reservations:
                if reservation.res_hour == res_hour and reservation.res_date == res_date:
                    return False  # Table déjà réservée à cette heure
        return True

    @staticmethod
    def extract_res_from_tab(tab_liste):

        reservation_liste = []

        for table in tab_liste:
            print(table)
            for reservation in table.reservations:
                print(reservation)
                if reservation not in reservation_liste:
                    reservation_liste.append(reservation)

        return  reservation_liste


    def supress_tables(self, tables):
        for table in tables:
            if table in self.tables:
                table.reservations.clear()
                self.tables.remove(table)
        print("tables et réservations supprimé")