from tkinter import *
from tkinter.filedialog import askopenfilename
import pyperclip as clip

# A Component for Postbox or for Selecting a Image and a Text Post of it


def PostBox(title, imageSelection=True):

    # Root of the window and it's property
    root = Tk()
    if imageSelection == True:
        root.geometry("500x500")
    else:
        root.geometry("500x400")
    root.title(title)
    root.resizable(width=False, height=False)
    PathOfImage = StringVar()

    # Function to Handle the Get Image Parameter
    def GetImage():
        pathOfImage = askopenfilename(
            filetypes=[("Select Images", ".png .jpg .jpeg")], multiple=True)
        PathOfImage.set(pathOfImage)

    # Dismiss this and move to the next step of Uploading
    def MoveToNext():
        Post = textbox.get(1.0, "end-1c")
        clip.copy(f'{Post}+{PathOfImage.get()}')
        root.destroy()

    # Main Label Component and it's root widgets
    labl = Label(root, text=f"{title} in the below TextBox")
    labl.config(font=("Courier", 12))
    labl.place(x=80, y=20)

    textbox = Text(root, height=15, width=60)
    textbox.place(x=8, y=60)

    if imageSelection == True:
        btn = Button(root, text="Select Image", command=GetImage)
        btn.place(x=30, y=325)

        labl = Label(root, text=f"Select Images to Upload")
        labl.config(font=("Courier", 11))
        labl.place(x=115, y=325)

        btn3 = Button(root, text="Next", command=MoveToNext)
        btn3.place(x=225, y=430)
    else:
        btn3 = Button(root, text="Next", command=MoveToNext)
        btn3.place(x=225, y=330)

    root.mainloop()
