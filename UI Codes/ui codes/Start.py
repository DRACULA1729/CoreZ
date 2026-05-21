import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import PIL to handle images
import time
import subprocess  # Import subprocess to run another script

def start_progress():
    progress_bar['value'] = 0  # Reset progress bar
    for i in range(101):  # Update progress bar from 0 to 100
        progress_bar['value'] = i
        percentage_label.config(text=f"{i}%")  # Update percentage label
        root.update()  # Update the GUI
        time.sleep(0.05)  # Sleep for 0.05 seconds (total 5 seconds)
    
    root.destroy()  # Destroy the window when progress is complete
    subprocess.Popen(['python', 'mainWindow.py'])  # Open mainWindow.py

# Create the main window
root = tk.Tk()
root.title("Initialising...")
root.geometry("600x400")  # Set the window size to 600x400

# Load the image
background_image = Image.open("images/intro.png")  # Make sure "intro.jpg" is in the same directory
bg_image = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0)  # Place the image at the top-left corner

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=550, mode='determinate', maximum=100)  # Adjust length to fit the window
progress_bar.place(relx=0.5, rely=0.9, anchor='center')  # Center the progress bar horizontally

# Create a label to display the percentage
percentage_label = tk.Label(root, text="0%", font=("Arial", 16), bg='white')  # Increase font size for better visibility
# Place the label 1 pixel above the progress bar
percentage_label.place(relx=0.95, rely=0.865, anchor='se')  # 0.905 is 1 pixel above 0.95

# Change the color and thickness of the progress bar (requires styling)
style = ttk.Style()
style.theme_use('clam')  # Use a theme that supports custom colors
style.configure("TProgressbar", troughcolor='lightgrey', background='darkblue', thickness=20)  # Set a darker color and thickness

# Start the progress automatically
start_progress()

# Run the application
root.mainloop()
