from tkinter import Label
from assets.contantes import *
from utils.ui_utils import configurer_scrollable_frame, displayEmpty


class NotificationsView:
    def __init__(self, notification_controller, frame):
        self.not_ctrl = notification_controller
        self.frame = frame


    def afficher_notifications(self):
        """Affiche les notifications reçues dans la dernière heure."""
        frame = configurer_scrollable_frame(self.frame)
        if not self.not_ctrl.notifications:
            displayEmpty(frame, EMPTY_NOTIFICATION)
        else:
            for message, timestamp in self.not_ctrl.notifications:
                Label(frame, text=f"{timestamp} - {message}", font=(
                    POLICE, 14), background="white", justify="left").pack(anchor="w", pady=5, padx=10)





