##alarm.py


import datetime
import time
import threading
import winsound  # For playing sound on Windows
import spacy

# Load Spacy English model
nlp = spacy.load("en_core_web_sm")

class Alarm:
    def __init__(self, alarm_time):
        self.alarm_time = alarm_time
        self.is_set = False

    def set_alarm(self):
        self.is_set = True
        print(f"Alarm set for {self.alarm_time.strftime('%Y-%m-%d %H:%M:%S')}")

    def check_alarm(self):
        current_time = datetime.datetime.now().time()
        if self.is_set and current_time.hour == self.alarm_time.hour \
                and current_time.minute == self.alarm_time.minute \
                and current_time.second == self.alarm_time.second:
            print("Alarm!")
            self.is_set = False
            # Play sound (Windows only)
            winsound.Beep(500, 1000)

def process_input(input_text):
    doc = nlp(input_text)
    time_entity = None
    for ent in doc.ents:
        if ent.label_ == "TIME":
            time_entity = ent.text
            break
    if time_entity is None:
        print("Unable to extract the time.")
        return None
    try:
        # Attempt to parse time in 12-hour clock format
        alarm_time = datetime.datetime.strptime(time_entity, '%I:%M %p')
    except ValueError:
        try:
            # Attempt to parse time in 24-hour clock format
            alarm_time = datetime.datetime.strptime(time_entity, '%H:%M')
        except ValueError:
            print("Invalid time format. Please use 'HH:MM' or 'HH:MM AM/PM' format.")
            return None
    
    # Get current date and combine with the parsed time
    current_date = datetime.datetime.now().date()
    alarm_time = datetime.datetime.combine(current_date, alarm_time.time())
    return alarm_time

def main(query=None):  # Modify main to accept an optional argument
    ##Set an alarm
    print("Setting an alarm. Please enter time (e.g., 'Set an alarm for 10:30 AM'):")
    input_text = query if query else input()
    alarm_time = process_input(input_text)
    if alarm_time is not None:
        alarm = Alarm(alarm_time)
        alarm.set_alarm()

    # Check alarms and timers every second
    while True:
        alarm.check_alarm()
        time.sleep(1)

# Example usage:
if __name__ == "__main__":
    main()
