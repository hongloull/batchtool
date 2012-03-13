#Description:get files from dir
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.22
#How to use :
import glob
import os
import Tkinter

def createWidgets():
    root = Tkinter.Tk()
    Dir = Tkinter.StringVar()
    #create the main Frame
    MainFrame = Tkinter.Frame(root)
    #Config Frame
    ConfigFrame = Tkinter.Frame(root)
    MayaLocLabel = Tkinter.Label(ConfigFrame, text='Directory:')
    MayaLocLabel.pack( side = Tkinter.LEFT )
    MayaLocEntry = Tkinter.Entry(ConfigFrame,textvariable=Dir,width=50)
    MayaLocEntry.pack( side = Tkinter.LEFT )
    MayaLocButton = Tkinter.Button(ConfigFrame,text='Set',width=10,command=setDirFunc)
    MayaLocButton.pack( side = Tkinter.LEFT )
    ConfigFrame.pack()
		
def setDirFunc():
    mayaLoc = tkFileDialog.askdirectory(title = 'Maya Location')
    MayaLoc.set(mayaLoc)
    

dir = '/mnt/data/tutorial/Work_flow/mayaProject/sourceimages/Approved/*/sourceimages/*.tga'
def getFileFromDir(dir):    
    #func for get files in selected folder
    for file in glob.glob(dir):
        print file
    return glob.glob(dir)


