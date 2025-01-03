# utils/formular_utils.py
from datetime import datetime, timedelta
from assets.contantes import *
from tkinter import *
from tkcalendar import Calendar
from tkinter import ttk

def ajouter_champ_nom(parent):
    """Ajoute un champ pour le nom de réservation."""
    frame_nom = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_nom.pack(fill="x", pady=10)
    Label(frame_nom, text="Nom de la réservation :", font=(POLICE, 16),
          background=LIGHT_CREAM_COLOR).pack(side="left", padx=10)

    nom_var = StringVar()
    Entry(frame_nom, textvariable=nom_var, font=(
        POLICE, 16), width=20).pack(side="left", padx=10)
    return nom_var


def ajouter_calendrier(parent):
    """Ajoute un calendrier pour choisir une date."""
    frame_cal = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_cal.pack(side="left", fill="y", padx=40)

    Label(frame_cal, text="Choisissez une date :", font=(
        POLICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)
    cal = Calendar(frame_cal, selectmode="day", mindate=datetime.now(),
                   maxdate=datetime.now() + timedelta(days=60))
    cal.pack()
    return cal


def ajouter_choix_horaires(parent):
    """Ajoute les créneaux horaires matin et soir avec des boutons radio en grille."""
    frame_heures = Frame(parent, background=LIGHT_CREAM_COLOR)
    frame_heures.pack(side="right", fill="both", padx=20)

    Label(frame_heures, text="Choisissez une heure :", font=(
        POLICE, 16), background=LIGHT_CREAM_COLOR).pack(pady=10)

    time_slots = generate_time_slots()
    selected_time_var = StringVar(value="")

    for label, slots in time_slots.items():
        Label(frame_heures, text=label, font=(POLICE, 14, "bold"),
              background=LIGHT_CREAM_COLOR).pack(pady=5)

        slot_frame = Frame(frame_heures, background=LIGHT_CREAM_COLOR)
        slot_frame.pack(pady=5, fill="x")

        # Afficher les créneaux horaires dans une grille
        max_columns = 4  # Nombre maximal de colonnes par ligne
        for index, slot in enumerate(slots):
            row, col = divmod(index, max_columns)
            ttk.Radiobutton(
                slot_frame,
                text=slot,
                variable=selected_time_var,
                value=slot
            ).grid(row=row, column=col, padx=5, pady=5, sticky="w")

    return selected_time_var


def generate_time_slots():
    """Génère des créneaux horaires matin et soir."""
    def slots(start, end):
        while start <= end:
            yield start.strftime("%H:%M")
            start += timedelta(minutes=30)

    return {
        "Matin :": list(slots(datetime.strptime("10:00", "%H:%M"), datetime.strptime("13:30", "%H:%M"))),
        "Soir :": list(slots(datetime.strptime("18:00", "%H:%M"), datetime.strptime("21:30", "%H:%M"))),
    }