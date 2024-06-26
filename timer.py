##timer.py

import datetime
import time
import threading
import winsound  # For playing sound on Windows
import spacy

# Load Spacy English model
nlp = spacy.load("en_core_web_sm")

class Timer:
    def __init__(self, duration_seconds):
        self.duration_seconds = duration_seconds
        self.start_time = None
        self.timer_thread = None
        self.is_running = False

    def _timer_callback(self):
        self.is_running = True
        self.start_time = time.time()
        time.sleep(self.duration_seconds)
        self.is_running = False
        print("Timer finished!")

    def start(self):
        if not self.is_running:
            self.timer_thread = threading.Thread(target=self._timer_callback)
            self.timer_thread.start()
        else:
            print("Timer is already running.")

    def stop(self):
        if self.is_running:
            self.timer_thread.join()
            self.is_running = False
            print("Timer stopped.")
        else:
            print("Timer is not running.")

def process_input(input_text):
    # Use SpaCy to process user input and extract numerical values and units of time
    doc = nlp(input_text)
    duration = None
    for token in doc:
        if token.pos_ == "NUM":
            duration = float(token.text)
        elif token.pos_ == "NOUN" and token.text.lower() in ["second", "seconds", "minute", "minutes", "hour", "hours"]:
            if token.text.lower() in ["second", "seconds"]:
                duration *= 1
            elif token.text.lower() in ["minute", "minutes"]:
                duration *= 60
            elif token.text.lower() in ["hour", "hours"]:
                duration *= 3600
    return duration

def main(query=None):  # Modify main to accept an optional argument
    # Check if a query is provided
    if query:
        duration = process_input(query)
        if duration:
            # Set a timer based on the provided query
            timer = Timer(duration)
            timer.start()

            # Check the timer every second
            while timer.is_running:
                time.sleep(1)
            print("Timer stopped.")
        else:
            print("No duration specified.")
    else:
        # Prompt the user to input the duration in natural language

        duration_text = input()
        duration = process_input(duration_text)
        if duration:
            # Set a timer based on the user input
            timer = Timer(duration)
            timer.start()

            # Check the timer every second
            while timer.is_running:
                time.sleep(1)
            print("Timer stopped.")
        else:
            print("No duration specified.")

# Example usage:
if __name__ == "__main__":
    main()
