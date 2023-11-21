import json
from datetime import datetime, timedelta
import time

def execute_routine(routine):
    print(f"Ejecutando rutina {routine['id']}")

def main():
    # Load the JSON file
    with open("execution.json", "r") as file:
        routines = json.load(file)

    while True:
        # Get the current time
        current_time = datetime.now().strftime("%H:%M")

        # Check if the current time matches any routine
        for routine in routines:
            if routine["hour"] == current_time:
                execute_routine(routine)

        # Wait for a minute before checking again
        time.sleep(60)

if __name__ == "__main__":
    main()
