# Import module
try:
    from tkinter import *
except ImportError:
    print("tk not Found. Try installing it via your package manager")
    import sys
    sys.exit(8)
from tkinter.scrolledtext import ScrolledText
import pyperclip as clip
from tkinter import ttk


def GetUserTag(options, title):

    # Define and Instantiate a particular window size with non resizable window
    root = Tk()
    root.geometry("200x200")
    root.title(title)
    root.resizable(width=False, height=False)

    # onclick get all the selected tags and then copy it to clipboard
    def show():
        overallText = ""
        if clicked.get() != "Select the Tag":
            overallText += clicked.get()
            label.config(text=clicked.get())
        clip.copy(overallText)
        root.destroy()

    # create a temporary variable to store the tag and set it a default value
    clicked = StringVar()
    clicked.set("Select the Tag")

    # Pack and design all the components of a window
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    button = Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()

    # Run it indefenite number of times
    root.mainloop()


# Get all the reddit subs to which we want to Post the particular post
def GetRedditSub(options: list):

    # Create a window with a specific size and not resizable
    root = Tk()
    root.config(width=500, height=len(options)*10)
    root.geometry(f"500x500")
    root.resizable(width=False, height=False)

    # create a list of Stringvar to choose the option selected
    optionCheckBox = {f"{options[0]}": IntVar()}
    for i in options:
        if i != options[0]:
            optionCheckBox[f"{i}"] = IntVar()

    # onclick to handle the checkbox
    def show():
        overallText = ""
        for key, value in optionCheckBox.items():
            val = value.get()
            if val != 0:
                overallText += f"{key}+"
        clip.copy(overallText)
        root.destroy()

    # variable to check to what to select and set it to a default value
    clicked = StringVar()
    clicked.set("Select the Tag")

    # Design and pack all the components
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    text = ScrolledText(root, width=50, height=25)
    text.pack()
    for key, value in optionCheckBox.items():
        text.window_create('end', window=Checkbutton(text=key, variable=value))
    Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()

    # Run it indefenitly times
    root.mainloop()


def GetRedditTag(options: list):

    # Create a window with a specific size and not resizable
    root = Tk()
    root.geometry("200x200")
    root.resizable(width=False, height=False)

    # coopy all the tags on click
    def show():
        overallText = ""
        if clicked.get() != "Select the Tag":
            overallText += clicked.get()
            label.config(text=clicked.get())
            label.config(text=clicked.get())
        clip.copy(overallText)
        root.destroy()

    # variable to check to what to select and set it to a default value
    clicked = StringVar()
    clicked.set("Select the Tag")

    # Design and pack all the components
    drop = ttk.Combobox(root, textvariable=clicked, values=options)
    drop.pack()
    Button(root, text="Next", command=show).pack()
    label = Label(root, text=" ")
    label.pack()

    # Run it indefenitly times
    root.mainloop()
