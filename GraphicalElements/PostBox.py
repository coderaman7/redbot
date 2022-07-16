import sqlite3
import sys
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import pyperclip as clip
import pymsgbox as pg


def PostBox(title):
    root = Tk()
    root.geometry("500x500")
    root.title(title)
    root.resizable(width=False, height=False)
    PathOfImage = StringVar()

    def GetImage():
        pathOfImage = askopenfilename(
            filetypes=[("Select Images", ".png .jpg .jpeg")], multiple=True)
        PathOfImage.set(pathOfImage)

    def MoveToNext():
        Post = textbox.get(1.0, "end-1c")
        clip.copy(f'{Post}+{PathOfImage.get()}')
        root.destroy()

    labl = Label(root, text=f"{title} in the below TextBox")
    labl.config(font=("Courier", 12))
    labl.place(x=80, y=20)

    textbox = Text(root, height=15, width=60)
    textbox.place(x=8, y=60)

    btn = Button(root, text="Select Image", command=GetImage)
    btn.place(x=30, y=325)

    labl = Label(root, text=f"Select Images to Upload")
    labl.config(font=("Courier", 11))
    labl.place(x=115, y=325)

    btn3 = Button(root, text="Next", command=MoveToNext)
    btn3.place(x=225, y=430)

    root.mainloop()