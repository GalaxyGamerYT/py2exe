from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
import PyInstaller
import PyInstaller.__main__
import PyInstaller.exceptions
from os.path import exists,isdir,join
from os import remove,listdir,replace,removedirs

from settings import *

name = None
file = None

def removeTempFolders(path):
    content = listdir(path)
    for i in content:
        if isdir(i):
            content2 = listdir(i)
            for i2 in content2:
                remove(i2)
    removedirs(path)

def removeTempFiles():
    if name != "":
        specFile = f"{name}.spec"
        buildFile = f"{name}.exe"
    else:
        projectName = (file.split(file))[1].split('.py')[0]
        specFile = f"{projectName}.spec"
        buildFile = f"{projectName}.exe"
    
    if exists(workpath["custom"]):
        removeTempFolders(workpath["custom"])
    elif exists(f"{workpath['default']}"):
        remove(workpath["default"])
    
    if exists(specpath["custom"]):
        removeTempFolders(specpath["custom"])
    elif exists(f"{join(specpath['default'],specFile)}"):
        remove(join(specpath['default'],specFile))
    
    if exists(distpath["custom"]):
        replace(join(distpath["custom"],buildFile),join(currentDirectory,buildFile))
        remove(distpath["custom"])
    elif exists(distpath["default"]):
        replace(join(distpath["default"],buildFile),join(currentDirectory,buildFile))
        remove(distpath["default"])

def removeOutputLabel(label:Label):
    label["text"]=""

def selectFile(type:str):
    global file
    global icon
    
    if type == "python":
        fileTypes = (
            ('python files', '*.py'),
            ('all files', '*.*')
        )
    elif type == "icon":
        fileTypes = (
            ('ico files', '*.ico'),
            ('exectuable files', '*.exe'),
            ('all files', '*.*')
        )
    
    fileName = filedialog.askopenfilename(
        title="Select a file",
        initialdir=currentDirectory,
        filetypes=fileTypes
    )
    
    if type == "python":
        fileEntry.delete(0,END)
        fileEntry.insert(END,fileName)
    elif type == "icon":
        iconEntry.delete(0,END)
        iconEntry.insert(END,fileName)
    
    showinfo(
        title="Selected File",
        message=fileName
    )

def submit():
    global name
    global file
    
    if customDirectories:
        localDispath = distpath["custom"]
        localWorkpath = workpath["custom"]
        localSpecpath = specpath["custom"]
    else:
        localDispath = distpath["default"]
        localWorkpath = workpath["default"]
        localSpecpath = specpath["default"]
    
    args = [
        "--onefile",
        "--clean",
        f"--distpath={localDispath}",
        f"--workpath={localWorkpath}",
        f"--specpath={localSpecpath}",
        "--noconfirm"
    ]
    
    file = fileEntry.get()
    ui = uiCombo.current()
    name = nameEntry.get()
    icon = iconEntry.get()
    
    if file != "":
        
        if exists(file):
            if ui == 0:
                args.append("-c")
            elif ui == 1:
                args.append("-w")
            
            if name != "":
                args.append(f"-n {name}")
            
            if icon != "":
                if exists(file):
                    args.append(f"-i {icon}")
                else:
                    outputLabel["text"] = "Icon File Does Not Exist"
                    outputLabel["fg"] = errorColour
                    return
            
            args.append(file)
            print(args)
            
            try:
                PyInstaller.__main__.run(args)
            except PyInstaller.exceptions.ExecCommandFailed as e:
                outputLabel["text"] = e
                outputLabel["fg"] = errorColour
            else:
                outputLabel["text"] = "Done"
                outputLabel["fg"] = completedColour
            
        else:
            outputLabel["text"] = "File Does Not Exist"
            outputLabel["fg"] = errorColour
    else:
        outputLabel["text"] = "No File Selected"
        outputLabel["fg"] = errorColour
    
    # removeTempFiles()
    root.after(5000, lambda: removeOutputLabel(outputLabel))

def help():
    helpWindow = Toplevel(root)
    helpWindow.title("Help Page")
    helpWindow.resizable(True,True)
    helpWindow.geometry(getWindowSize("center",helpWindow))
    
    # WIP
    
    Label(helpWindow,text="W.I.P").pack()
    
    # Tab Control
    
    tabControl = ttk.Notebook(helpWindow)
    
    # Home Tab
    
    homeTab = Frame(tabControl)
    tabControl.add(homeTab, text="Home")
    Label(homeTab,text="HELP PAGE").pack()
    
    # Files Tab
    
    filesTab = Frame(tabControl)
    tabControl.add(filesTab, text="Files")
    
    # Types Tab
    
    typesTab = Frame(tabControl)
    tabControl.add(typesTab, text="Types")
    
    # Icons Tab
    
    iconsTab = Frame(tabControl)
    tabControl.add(iconsTab, text="Icons")
    
    tabControl.pack(expand=1, fill="both")

def steps():
    stepsWindow = Toplevel(root)
    stepsWindow.title("Step By Step")
    stepsWindow.resizable(True,True)
    stepsWindow.geometry(getWindowSize("center",stepsWindow))
    
    Label(stepsWindow,text="Step By Step Guide").pack()
    
    # WIP
    
    Label(stepsWindow,text="W.I.P").pack()

def settings():
    settingsWindow = Toplevel(root)
    settingsWindow.title("Settings")
    settingsWindow.resizable(True,True)
    settingsWindow.geometry(getWindowSize("center",settingsWindow))
    
    Label(settingsWindow,text="Settings").pack()
    
    # WIP
    
    Label(settingsWindow,text="W.I.P").pack()

root = Tk()
root.title(titleText)
root.geometry(getWindowSize("center",root))
root.resizable(False,False)
root.configure(background=backgroundColour)

title = Label(root,text="Python 2 Executable",font=titleFont)
title.grid(row=0,column=0,pady=yPadding)

# Menu Bar

menuBar = Menu(root)
root.config(menu=menuBar)

menuBar.add_command(
    label="Settings",
    command=settings
)

menuBar.add_command(
    label="Steps",
    command=steps
)

menuBar.add_command(
    label="Help",
    command=help
)

# File

fileFrame = Frame(root)
fileFrame.grid(row=1,column=0,pady=yPadding)
fileFrame.configure(width=frameSize,border=frameborder,borderwidth=frameBorderWidth)

fileLabel = Label(fileFrame,text="Main File")
fileLabel.grid(row=0,column=0,padx=xFramePadding)

# File Sub Frame

fileSubFrame = Frame(fileFrame)
fileSubFrame.grid(row=0,column=1,padx=xFramePadding)

fileEntry = Entry(fileSubFrame)
fileEntry.grid(row=0,column=0)
fileSelectFileBtn = Button(fileSubFrame,text="Select File",command=lambda: selectFile("python"))
fileSelectFileBtn.grid(row=0,column=1)
Label(fileSubFrame,text="*",fg="red",font=labelFont).grid(row=0,column=2)

# UI

uiFrame = Frame(root)
uiFrame.grid(row=2,column=0,pady=yPadding)
uiFrame.configure(width=frameSize,border=frameborder,borderwidth=frameBorderWidth)

uiComboLabel = Label(uiFrame,text="Type")
uiComboLabel.grid(row=0,column=0,padx=xFramePadding)

# UI Sub Frame

uiSubFrame = Frame(uiFrame)
uiSubFrame.grid(row=0,column=1,padx=xFramePadding)

uiCombo = ttk.Combobox(
    uiSubFrame,
    state="readonly",
    values=uiValues
)
uiCombo.grid(row=0,column=0)
uiCombo.current(1)
Label(uiSubFrame,text="*",fg="red",font=labelFont).grid(row=0,column=1)

# Name

nameFrame = Frame(root)
nameFrame.grid(row=3,column=0,pady=yPadding)
nameFrame.configure(width=frameSize,border=frameborder,borderwidth=frameBorderWidth)

nameLabel = Label(nameFrame,text="Name")
nameLabel.grid(row=0,column=0,padx=xFramePadding)
nameEntry = Entry(nameFrame)
nameEntry.grid(row=0,column=1,padx=xFramePadding)

# Icon

iconFrame = Frame(root)
iconFrame.grid(row=4,column=0,pady=yPadding)
iconFrame.configure(width=frameSize,border=frameborder,borderwidth=frameBorderWidth)

iconLabel = Label(iconFrame,text="Icon")
iconLabel.grid(row=0,column=0,padx=xFramePadding)

# Icon Sub Frame

iconSubFrame = Frame(iconFrame)
iconSubFrame.grid(row=0,column=1,padx=xFramePadding)

iconEntry = Entry(iconSubFrame)
iconEntry.grid(row=0,column=0)
iconSelectFileBtn = Button(iconSubFrame,text="Select File",command=lambda: selectFile("icon"))
iconSelectFileBtn.grid(row=0,column=1)

# Required Text

Label(root,text="* Required",fg="red").grid(row=98,column=0)

# Submit

submitBtn = Button(root,text="Submit",font=btnFont,command=submit)
submitBtn.grid(row=99,column=0,pady=yPadding)

# Output

outputLabel = Label(root,text="")
outputLabel.grid(row=100,column=0,pady=yPadding)

root.mainloop()