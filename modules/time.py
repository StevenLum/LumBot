from datetime import datetime


class Time:
    def get_date(self):
        return datetime.now().strftime("%d.%m.%Y")

    def get_short_time(self):
        return datetime.now().strftime("%H.%M")

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")

    def get_datetime(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #Subtracts the current users last accepted .daily call to the current time
    def subtract(self, string):
        return datetime.strptime(
            self.get_datetime(), "%Y-%m-%d %H:%M:%S"
            ) - datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
        

    def delta(self, time):
        time = datetime.strptime("12:00:00", "%H:%M:%S") - time
        return time.strftime("%H:%M:%S")