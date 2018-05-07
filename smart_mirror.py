# Script to control updating the display
from tkinter import *
from settings import Settings
from main_panel import Main
import time


# Creates window
root = Tk()
root.title("Weather App")
root.configure(background = 'black')

# Establish settings variable
settings = Settings()

# Create panel class with settings
Main = Main(settings)

# Call panel function to create itself
Main.create(root)
root.mainloop()




