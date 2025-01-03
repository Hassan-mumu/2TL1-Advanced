# utils/ui_utils.py
from tkinter import *
from assets.contantes import *
from models.reservation import Reservation
from models.table import Table

def configurer_scrollable_frame(frame):
    """Configure le canvas et le frame scrollable de la frame de droite."""
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = Canvas(frame, background=LIGHT_CREAM_COLOR)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, background=LIGHT_CREAM_COLOR)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Ajuster la taille initiale
    scrollable_frame.update_idletasks()
    canvas.config(width=scrollable_frame.winfo_width(), height=scrollable_frame.winfo_height())

    return scrollable_frame

def create_button_menu(frame, text, font, height, width, background, command, row, column):
    Button(
        frame, text=text, font=font, height=height, width=width, background=background, command=command
    ).grid(pady=20, padx=10, row=row, column=column)

def displayEmpty(parent_frame, message):
    """Affiche un message indiquant qu'il n'y a pas de données à afficher."""
    Label(parent_frame, text=message, font=(POLICE, 20), background=LIGHT_CREAM_COLOR, justify="center"
          ).pack(pady=20, padx=20, anchor="center")

def afficher_details_reservation(cadre, reservation: Reservation):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Name : {reservation.name}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Table(s) : {reservation.table}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Date : {reservation.date_representation()}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Hour : {reservation.hour_representation()}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)

def afficher_details_table(cadre, table: Table):
    """Affiche les informations d'une table dans le cadre donné."""
    Label(cadre, text=f"Table ID : {table.t_id}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"Places : {table.seat_nbr}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)
    Label(cadre, text=f"État : {table.state}", font=(
        POLICE, 16), background="white").pack(anchor="w", padx=10)

def afficher_confirmation(frame, reservation: Reservation):
    """Affiche un message de confirmation et revient à l'écran des tables."""
    frame = configurer_scrollable_frame(frame)

    frame_reservation = Frame(frame, background=LIGHT_CREAM_COLOR)
    frame_reservation.pack(pady=20)

    Label(
        frame_reservation,
        text=f"Réservation confirmée pour la Table {reservation.table}",
        font=(POLICE, 20, "bold"), background=LIGHT_CREAM_COLOR
    ).pack(pady=20)

    Label(
        frame_reservation,
        text=f"Date : {reservation.date_representation()}\nHeure : {reservation.hour_representation()}\nNom : {reservation.name}",
        font=(POLICE, 16), background=LIGHT_CREAM_COLOR
    ).pack(pady=10)

def to_minute(t) :
  return t.hour * 60 + t.minute