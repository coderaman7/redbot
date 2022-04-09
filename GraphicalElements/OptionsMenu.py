# Import module
from tkinter import *
import pyperclip as clip

def GetUserTag(options: list):
    root = Tk()
    root.geometry("200x200")
    def show():
        overallText=""
        if clicked.get() != "Select the Tag":
            overallText += clicked.get()
            label.config(text=clicked.get())
        if clicked1.get() != "Select the Tag":
            overallText += "+"
            overallText += clicked1.get()
            label1.config(text=clicked1.get())
        if clicked2.get() != "Select the Tag":
            overallText += "+"
            overallText += clicked2.get()
            label2.config(text=clicked2.get())
        clip.copy(overallText)
        root.destroy()
        # root.quit()
        # root.update()
    clicked = StringVar()
    clicked1 = StringVar()
    clicked2 = StringVar()
    clicked.set("Select the Tag")
    clicked1.set("Select the Tag")
    clicked2.set("Select the Tag")
    drop = OptionMenu(root, clicked, *options)
    drop.pack()
    drop1 = OptionMenu(root, clicked1, *options)
    drop1.pack()
    drop2 = OptionMenu(root, clicked2, *options)
    drop2.pack()
    button = Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()
    label1 = Label(root, text=" ")
    label1.pack()
    label2 = Label(root, text=" ")
    label2.pack()
    root.mainloop()