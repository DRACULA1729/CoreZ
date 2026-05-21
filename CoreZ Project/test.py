# Import Module
from tkinter import *

# Create Object
root = Tk()

# Add Title
root.title('On/Off Switch!')

# Add Geometry
root.geometry("500x300")

# Keep track of the button state on/off
#global is_on
is_on = True

# Create Label
my_label = Label(root, 
	text = "The Switch Is On!", 
	fg = "green", 
	font = ("Helvetica", 32))

my_label.pack(pady = 20)

# Define our switch function
def switch():
	global is_on
	
	# Determine is on or off
	if is_on:
		on_button.config(image = off)
		my_label.config(text = "The Switch is Off", 
						fg = "grey")
		is_on = False
	else:
	
		on_button.config(image = on)
		my_label.config(text = "The Switch is On", fg = "green")
		is_on = True

# Define Our Images
# TODO: replace placeholders with real on/off icon paths before running
on = PhotoImage(file = "<TODO: path/to/on.png>")
off = PhotoImage(file = "<TODO: path/to/off.png>")

# Create A Button
on_button = Button(root, image = on, bd = 0,
				command = switch)
on_button.pack(pady = 50)

# Execute Tkinter
root.mainloop()
