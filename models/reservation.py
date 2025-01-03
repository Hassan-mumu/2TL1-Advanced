from datetime import datetime, date, time

class Reservation:
    id = 1

    def __init__(self, table, res_hour: datetime, res_date: datetime, name="defaultName", res_id=None, babychairs=0, state="W") -> object:
        """

        :rtype: object
        """
        self.__res_id = res_id if res_id else Reservation.id
        self.__name = name
        self.__table = table if isinstance(table, list) else [table]
        self.__state = state
        self.__res_hour = res_hour 
        self.__res_date = res_date
        self.__babychairs = babychairs
        
        if not isinstance(res_date, date):
            raise TypeError(f"{res_date} is {type(res_date)} not of datetime.date type")
        if not isinstance(res_hour, time):
            raise TypeError(f"{res_hour} is {type(res_hour)} not of datetime.time type")

        # Mise à jour des états des tables
        new_state = 'R' if self.name != "defaultName" else 'X'
        for tb in self.table:
            tb.state = new_state

        Reservation.id += 1
        print(f"La réservation {self.res_id} a été établie.")

    @property
    def res_id(self):
        return self.__res_id
    
    @property
    def name(self):
        return self.__name

    @property
    def table(self):
        return self.__table

    @property
    def state(self):
        return self.__state

    @property
    def res_hour(self):
        return self.__res_hour

    @property
    def res_date(self):
        return self.__res_date
    
    @property
    def babychairs(self):
        return self.__babychairs

    def hour_representation(self):
        return self.res_hour.strftime("%H:%M")

    def date_representation(self):
        return self.res_date.strftime("%d/%m/%y")

    def state_representation(self):
        if self.__state == 'W':
            return "En attente..."
        elif self.__state == 'P':
            return "En cours..."

    def change_state(self, new_state):
        if new_state == "P":
            self.__state = new_state
            for tb in self.table:
                tb.state = "X"
        elif new_state == 'T':
            for tb in self.table:
                tb.state = "V"
        else:
            print("Invalid state")


    def is_available(self):
        return all(map(lambda t : t.state != "X",  self.table))


    def __str__(self):
        return f"Nom : {self.name}\nTable(s) : {self.table}\nDate : {self.date_representation()}\nHeure : {self.hour_representation()}"

    def __repr__(self):
        return str(self)
