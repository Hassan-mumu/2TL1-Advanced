# app/main.py
from tkinter import Tk
from views.main_window import MainWindow
from controllers.reservation_controller import ReservationController
from controllers.table_controller import TableController
from controllers.notification_controller import NotificationController
from models.database_manager import  DatabaseManager
from assets.contantes import DARK_CREAM_COLOR


def main():
    # Créer la fenêtre principale
    fenetre = Tk()
    fenetre.geometry("1920x1080")
    fenetre.title("La bonne fourchette")
    fenetre.configure(background=DARK_CREAM_COLOR, pady=20)

    # Initialiser DatabaseManager
    database_manager = DatabaseManager()

    # Initialiser les contrôleurs
    table_controller = TableController(database_manager)
    reservation_controller = ReservationController(database_manager, table_controller)
    notification_controller = NotificationController(reservation_controller)

    # Initialiser la fenêtre principale
    main_window = MainWindow(fenetre, reservation_controller, table_controller, notification_controller)
    main_window.run()

    fenetre.mainloop()

    database_manager.save_tables(table_controller.tables)
    database_manager.save_reservations(reservation_controller.reservations)
    print("Données sauvegardées avec succès.")


if __name__ == "__main__":
    main()
