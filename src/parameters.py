import os
from datetime import date
import sys

class Parameters:
    def __init__(self):
        pass

        self.today = date.today().isoformat()

        # posts.py is inside /posts
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

        # Go up ONE level to project root
        self.PROJECT_ROOT = os.path.dirname(self.CURRENT_DIR)

        self.last_run_path = os.path.join(self.PROJECT_ROOT, "parameters", "dailyjsp", "last_run.txt")
        # counter_path = os.path.join(PROJECT_ROOT, "parameters", "movie", "counter.txt")


    def isValid(self):
        # Read last run date
        with open(self.last_run_path, "r") as t:
            last_run = t.read().strip()

        # Stop if already ran today
        if last_run == self.today:
            print("Already ran today. Exiting.")
            return False
        
        return True


    def updateParameters(self):
        #Update todays date in last run file
        with open(self.last_run_path, "w") as date:
            date.write(str(self.today))

        return True