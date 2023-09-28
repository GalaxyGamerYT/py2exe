from os import getcwd,path
from tkinter import Tk, Toplevel
from typing import Union

# Window

windowWidth=625
windowHeight=500
windowSize = f"{windowWidth}x{windowHeight}"
titleText = "Py2Exe"
# backgroundColour = "dark grey"
backgroundColour = None

def getWindowSize(args:str="",window:Union[Tk,Toplevel]=None)->str:
    if args == "center":
        return f"{windowSize}+{window.winfo_screenwidth()//2-windowWidth//2}+{window.winfo_screenheight()//2-windowHeight//2}"
    elif args == "":
        return windowSize

# Fonts

titleFont = ("arial",50)
labelFont = ("arial",25)
entryFont = ("arial",25)
btnFont = ("arial",25)

# Sizes

frameSize = 100
yPadding = 10

# Frames

xFramePadding = 10
frameborder = 2
frameBorderWidth = 2

# UI

uiValues = ["Text","Graphical"]

# Output

errorColour = "red"
completedColour = "green"

# PyInstaller

customDirectories = True
currentDirectory = getcwd()
workpath = {"default":path.join(currentDirectory,"build"), "custom":path.join(currentDirectory,"temp_build_folder")}
distpath = {"default":path.join(currentDirectory,"dist"), "custom":getcwd()}
specpath = {"default":currentDirectory, "custom":path.join(currentDirectory,"temp_spec_folder")}

