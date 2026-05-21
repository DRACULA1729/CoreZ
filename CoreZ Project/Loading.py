from tkinter import *
import os
from tkinter.ttk import Progressbar
from tkinter import ttk
loading = Tk()
loading.geometry("600x400+400+150")
loading.resizable(0,0)
bg = PhotoImage(file="Images/Intro.png", master=loading)
label_image = Label(loading, image=bg).pack()
progress_label = Label(loading, text="Loading....", font=('Comic Sans MS', 13, 'bold'), fg='#14183C', bg='#EFF0F6' )
progress_label.place(x=20, y=294)
#progress bar color selection
s = ttk.Style()
s.theme_use('alt')
s.configure("blue.Horizontal.TProgressbar", background='#14183C')
progress = ttk.Progressbar(loading, orient=HORIZONTAL,style='blue.Horizontal.TProgressbar' ,length=360, mode='determinate')
progress.place(x=160, y=300)
#remove windows lines or borders
loading.overrideredirect(1)
loading.wm_attributes("-topmost", True)
loading.lift()
loading.wm_attributes("-topmost", True)
loading.wm_attributes("-disabled", True)

def top():
    loading.withdraw()
    os.system("python gui.py")
    loading.destroy()

i = 0
def load():
    global i
    if i<=5:
        txt = "Loading..." + (str(20*i)+ "%")
        progress_label.config(text=txt)
        progress_label.after(900,load)
        progress['value'] = 20*i
        i += 1
    else:
        top()    
load()



loading.mainloop()