from datetime import *

from utils.ui_utils import to_minute

from assets.contantes import HOUR_TO_MINUTE, LATE_RESERVATION


class NotificationController:
    def __init__(self, reservation_controller):
        self.__notifications = []  # Liste des notifications envoyées ou reçues
        self.res_ctrl = reservation_controller

    @property
    def notifications(self):
        return self.__notifications

    def check_status(self):
        """Vérifie l'état des tables et génère des notifications."""
        current_time = datetime.now().time()

        updated = False
        for reservation in self.res_ctrl.reservations:

            if  to_minute(current_time) - to_minute(reservation.res_hour) >= LATE_RESERVATION and reservation.is_available():
                message = f"Rappel : Reservation {reservation.res_id} pour {reservation.res_hour} n'est toujours pas occupé."
                self.add_notification(message)

    def add_notification(self, message):
        notif_time = datetime.now().strftime('%H:%M')
        self.__notifications.insert(0,(message, notif_time))

    def supprimer_notification(self, notification):
        """Supprime une notification de la liste."""
        if notification in self.__notifications:
            self.__notifications.remove(notification)
            print(f"Notification supprimée : {notification['message']}")
