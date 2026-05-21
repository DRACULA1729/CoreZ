import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL to handle images

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# Create the main window
root = tk.Tk()
root.title("Initialising...")
root.geometry("600x400")  # Set the window size to 600x400

# Load the image
background_image = Image.open(os.path.join(SCRIPT_DIR, "images", "intro.png"))
bg_image = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0)  # Place the image at the top-left corner

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=550, mode='determinate', maximum=100)
progress_bar.place(relx=0.5, rely=0.9, anchor='center')

# Create a label to display the percentage
percentage_label = tk.Label(root, text="0%", font=("Arial", 16), bg='white')
percentage_label.place(relx=0.95, rely=0.865, anchor='se')

# Change the color and thickness of the progress bar (requires styling)
style = ttk.Style()
style.theme_use('clam')
style.configure("TProgressbar", troughcolor='lightgrey', background='darkblue', thickness=20)


def step_progress(i=0):
    if i > 100:
        subprocess.Popen(
            [sys.executable, os.path.join(SCRIPT_DIR, "mainWindow.py")],
            cwd=SCRIPT_DIR,
        )
        root.destroy()
        return
    progress_bar['value'] = i
    percentage_label.config(text=f"{i}%")
    root.after(50, step_progress, i + 1)


# Drive progress via the Tk event loop instead of blocking with time.sleep
root.after(0, step_progress)

# Run the application
root.mainloop()
