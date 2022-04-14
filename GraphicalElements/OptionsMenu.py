# Import module
from tkinter import *
import pyperclip as clip
from tkinter import ttk

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
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    # drop1 = ttk.Combobox(root, textvariable=clicked1, values=options)
    # drop1.pack()
    # drop2 = ttk.Combobox(root, textvariable=clicked2, values=options)
    # drop2.pack()
    button = Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()
    label1 = Label(root, text=" ")
    label1.pack()
    label2 = Label(root, text=" ")
    label2.pack()
    root.mainloop()


def GetRedditSub(options: list):
    root = Tk()
    root.config(width=500,height=len(options)*10)
    root.geometry(f"500x{len(options)*30}")

    optionCheckBox = {f"{options[0]}":IntVar()}
    for i in options:
        if i != options[0]:
            optionCheckBox[f"{i}"] = IntVar()

    def show():
        overallText = ""
        for key, value in optionCheckBox.items():
                val = value.get()
                if val != 0:
                    overallText += f"{key}+"
        clip.copy(overallText)
        root.destroy()
        # root.quit()
        # root.update()
    clicked = StringVar()
    clicked.set("Select the Tag")
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    for key, value in optionCheckBox.items():
        ctrl = Checkbutton(text=key, variable=value)
        ctrl.pack()
    button = Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()
    root.mainloop()



def GetRedditTag(options: list):
    root = Tk()
    root.geometry("200x200")

    def show():
        overallText = ""
        if clicked.get() != "Select the Tag":
            overallText += clicked.get()
            label.config(text=clicked.get())
            label.config(text=clicked.get())
        clip.copy(overallText)
        root.destroy()
        # root.quit()
        # root.update()
    clicked = StringVar()
    clicked.set("Select the Tag")
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    button = Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()
    root.mainloop()