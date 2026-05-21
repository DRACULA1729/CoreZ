import os
import sys
import subprocess
from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create a main window
root = tk.Tk()

# Set the window title
root.title("Boosting RAM...")
root.geometry("600x400")

# Load the background image
bg = PhotoImage(file=os.path.join(SCRIPT_DIR, "images", "background.png"))

# Create a label to display the background image
label = Label(root, image=bg)
label.place(x=0, y=0)

# Add a heading label
heading_label = Label(root, text="Boosting RAM...", font=("sans-serif", 28, "bold"), fg="black", bg="white")
heading_label.place(relx=0.5, rely=0.3, anchor=CENTER)

# Add a subheading label
subheading_label = Label(root, text="Please wait while we optimize your system...", font=("Arial", 14), fg="green", bg="white")
subheading_label.place(relx=0.36, rely=0.73, anchor=CENTER)

# Create a progress bar
progress = Progressbar(root, orient=HORIZONTAL, length=550, mode='determinate', value=0)

# Place the progress bar in the center of the window
progress.place(relx=0.5, rely=0.8, anchor=CENTER)

# Create a label to display the percentage
percentage_label = Label(root, text="0%", font=("Arial", 16), fg="green", bg="white")
percentage_label.place(x=520, y=275)

# Function to show the success dialog
def show_success_dialog():
    # Hide the main window
    root.withdraw()

    # Create a new Toplevel window
    success_dialog = Toplevel(root)
    success_dialog.title("Success")
    success_dialog.geometry("600x400")  # Same size as the main window

    # Load the same background image
    bg_success = PhotoImage(file=os.path.join(SCRIPT_DIR, "images", "background.png"))

    # Create a label to display the background image
    bg_label = Label(success_dialog, image=bg_success)
    bg_label.place(x=0, y=0)
    bg_label.image = bg_success  # Keep a reference to avoid garbage collection

    # Add a success message
    success_label = Label(success_dialog, text="RAM Boosted Successfully!", font=("sans-serif", 30, "bold"))
    success_label.place(relx=0.5, rely=0.3, anchor=CENTER)

    # Add a button to return to the main menu
    return_button = Button(success_dialog, text="Return to Main Menu", font=("Arial", 12), command=lambda: go_to_main_menu(success_dialog))
    return_button.place(relx=0.5, rely=0.6, anchor=CENTER)

# Function to go to the main menu
def go_to_main_menu(dialog):
    dialog.destroy()  # Close the success dialog
    root.destroy()    # Close the main window completely
    subprocess.Popen(
        [sys.executable, os.path.join(SCRIPT_DIR, "mainWindow.py")],
        cwd=SCRIPT_DIR,
    )
    
# Function to update the progress bar and percentage
def update_progress():
    global progress_value
    progress_value += 2  # Slowed down the increment
    progress['value'] = progress_value
    percentage_label['text'] = f"{progress_value}%"
    if progress_value < 100:
        root.after(100, update_progress)  # Slowed down the update interval
    else:
        show_success_dialog()  # Show the success dialog when progress is complete

# Start updating the progress bar and percentage
progress_value = 0
update_progress()

root.mainloop()