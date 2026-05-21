import engine 
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
#from PIL import ImageTk, Image
window = Tk()
window.geometry("900x600+220+65")
window.title("CoreZ Advance Security")
logo = PhotoImage(file="Images/Logo.png")
window.iconphoto(False , logo)
background = PhotoImage(file="Images/Frame 1.png")
Label_1 = Label(window,image=background)
Label_1.place(x=0,y=0)
window.resizable(0,0)
def openProtectionWindow():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Protection")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo1 = PhotoImage(file='Images/Protect.png')
    newWindow.iconphoto(False,logo1)
        # Creating a label widget and placing it in the window
    Lbl1 = Label(newWindow, text="This is Protection Window", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
 


 
    
def openSettingWindow():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Settings")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115") 
    newWindow.resizable(0,0)
    logo2 = PhotoImage(file='Images/Settings.png')
    newWindow.iconphoto(False,logo2)   
    Lbl1 = Label(newWindow, text="This is Settings Window", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
    

def openPrivacyWindow():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Privacy")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo3 = PhotoImage(file='Images/Privacy.png')
    newWindow.iconphoto(False,logo3)
    Lbl1 = Label(newWindow, text="This is Privacy Window", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
    

def openSupportWindow():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Support")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)    
    logo4 = PhotoImage(file='Images/Support.png')
    newWindow.iconphoto(False,logo4)
    Lbl1 = Label(newWindow, text="This is Support Window", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14),command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
     

def Quickscan():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Quick Scan")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo5 = PhotoImage(file='Images/Quickscan.png')
    newWindow.iconphoto(False,logo5)
    # Creating a label widget and placing it in the window
    Lbl1 = Label(newWindow, text="Quick Scan", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
     

def Fullscan():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Full Scan")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo6 = PhotoImage(file='Images/Fullscan.png')
    newWindow.iconphoto(False,logo6)
    # Creating a label widget and placing it in the window
    Lbl1 = Label(newWindow, text="Full Scan", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()


def JunkCleaner():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Junk Cleaner")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo7 = PhotoImage(file='Images/Junk.png')
    newWindow.iconphoto(False,logo7)
    # Creating a label widget and placing it in the window
    Lbl1 = Label(newWindow, text="Junk Cleaner", font=('Arial',14))
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    Lbl1.pack()
   
def Rambooster():
     
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(window)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("RAM Booster")
 
    # sets the geometry of toplevel
    newWindow.geometry("700x500+320+115")
    newWindow.resizable(0,0)
    logo8 = PhotoImage(file='Images/Rambooster.png')
    newWindow.iconphoto(False,logo8)
    # Create a label to display the output
    output_label = Label(newWindow, text="", font=('Arial', 14))
    output_label.pack(pady=20)

    # Get the output from the ramboost function
    output = engine.ramboost()  # Assuming this function returns a string

    # Set the output to the label
    output_label.config(text=output)
    # Creating a label widget and placing it in the window
    Lbl1 = Label(newWindow, text="RAM Booster", font=('Arial',14))
    Lbl1.pack()
    lbl = tk.Button(newWindow, text="Quit", font=('Arial',14), command=newWindow.destroy).place(x=300,y=100)
    
  


style = Style()
style.configure('A.TButton', font = 
                 ('Airal', 32), background='green')
style.configure('B.TButton', font = 
                 ('Airal', 32), background='red')
style.configure('C.TButton', font = 
                 ('Airal', 24), background='darkblue')
style.configure('W.TButton', font = 
                ('Helvetica', 14), background='white')
btn1 = Button(window, text = 'Dashboard', 
                style = 'W.TButton',
                command=window)
btn1.grid(row = 0, column = 3, padx = 100)
btn1.place(x=40,y=150)

btn2 = Button(window, text = 'Protection', 
                style = 'W.TButton',
             command =lambda:[openProtectionWindow(),window.grab_set()])
btn2.grid(row = 0, column = 3, padx = 100)
btn2.place(x=40,y=230)

btn3 = Button(window, text = 'Settings', 
                style = 'W.TButton',
             command = openSettingWindow)
btn3.grid(row = 0, column = 3, padx = 100)
btn3.place(x=40,y=310)

btn4 = Button(window, text = 'Privacy', 
                style = 'W.TButton',
             command = openPrivacyWindow)
btn4.grid(row = 0, column = 3, padx = 100)
btn4.place(x=40,y=390)

btn8 = Button(window, text = 'Support', 
                style = 'W.TButton',
             command = openSupportWindow)
btn8.grid(row = 0, column = 3, padx = 100)
btn8.place(x=40,y=470)

btn5 = Button(window, text = 'Quick Scan', 
                style = 'C.TButton',
             command = Quickscan)
btn5.grid(row = 0, column = 3, padx = 100)
btn5.place(x=320,y=200)

btn6 = Button(window, text = 'Full Scan', 
                style = 'C.TButton',
             command = Fullscan)
btn6.grid(row = 0, column = 3, padx = 100)
btn6.place(x=520,y=280)

btn7 = Button(window, text = 'Junk Cleaner', 
                style = 'C.TButton',
             command = JunkCleaner)
btn7.grid(row = 0, column = 3, padx = 100)
btn7.place(x=320,y=360)

btn9 = Button(window, text = 'RAM Booster', 
                style = 'C.TButton',
             command = lambda:[Rambooster(),engine.ramboost()])
btn9.grid(row = 0, column = 3, padx = 100)
btn9.place(x=520,y=440)      
      

window.mainloop()