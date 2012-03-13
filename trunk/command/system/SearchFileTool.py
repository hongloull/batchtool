#!/usr/bin/env python
#Description:get files from dir by func of 'glob.glob' and 'os.path.walk'
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.26
#How to use :
import glob
import os
import Tkinter
import tkFileDialog

class SearchFileTool:
	def __init__(self):
		self.CreateWidgets()
	def CreateWidgets(self):
		self.root = Tkinter.Tk()
		self.root.title('Search Tools V1.0')
		#def var
		self.Dir = Tkinter.StringVar()
		self.File = Tkinter.StringVar()
		self.Ext = Tkinter.StringVar()

		#create the main Frame
		MainFrame = Tkinter.Frame(self.root)		

		#Directory Frame
		DirectoryFrame = Tkinter.Frame(self.root)
		DirLabel = Tkinter.Label(DirectoryFrame, text='Directory:')
		DirLabel.pack( side = Tkinter.LEFT )
		self.DirEntry = Tkinter.Entry(DirectoryFrame,textvariable=self.Dir,width=50)
		self.DirEntry.pack( side = Tkinter.LEFT )
		DirButton = Tkinter.Button(DirectoryFrame,text='Set',width=10,command=self.setDirFunc)
		DirButton.pack( side = Tkinter.LEFT )
		DirectoryFrame.pack()

	        #Extension Frame
		ExtFrame = Tkinter.Frame(self.root)
		ExtLabel = Tkinter.Label(ExtFrame, text='Ext:')
		ExtLabel.pack( side = Tkinter.LEFT )
		self.ExtEntry = Tkinter.Entry(ExtFrame,textvariable=self.Ext,width=50)
		self.ExtEntry.pack( side = Tkinter.LEFT )
		ExtFrame.pack()

		#Search Frame
		SearchFrame = Tkinter.Frame(self.root)
		GlobSearchButton = Tkinter.Button(SearchFrame,text='Glob Search',width=16,command=self.globSearch)
		GlobSearchButton.pack( side = Tkinter.LEFT )                
		OsPathWalkSearchButton = Tkinter.Button(SearchFrame,text='Os Path Walk',width=16,command=self.OsPathWalkSearch)
		OsPathWalkSearchButton.pack( side = Tkinter.LEFT )                
		SearchFrame.pack()		

		#file list label Frame
		FileListFrame = Tkinter.Frame(self.root)
		FileListLabel = Tkinter.Label(FileListFrame,text='File List:')
		FileListLabel.pack( side = Tkinter.LEFT )
		FileListFrame.pack()
		#file Frame
		FileFrame = Tkinter.Frame(self.root)
		FileScrollbar = Tkinter.Scrollbar(FileFrame)
		FileScrollbar.pack(side = Tkinter.RIGHT,fill = Tkinter.Y)
		self.FileText = Tkinter.Text(FileFrame,yscrollcommand=FileScrollbar.set)
		self.FileText.pack()
		FileScrollbar.config(command=self.FileText.yview)
		FileFrame.pack()
                
		#batch file Frame
		BatchFileFrame = Tkinter.Frame(self.root)
		ClearFileButton = Tkinter.Button(BatchFileFrame,text='Clear File List',width=20,command=self.clearFileButtonFunc)
		ClearFileButton.pack( side = Tkinter.LEFT )
		BatchFileButton = Tkinter.Button(BatchFileFrame,text='Save File List',width=20,command=self.saveBatchFileButtonFunc)
		BatchFileButton.pack( side = Tkinter.LEFT )		
		BatchFileFrame.pack()

		MainFrame.pack(fill=Tkinter.BOTH,expand=Tkinter.YES)

        def clearFileButtonFunc(self):    
            #func for get files in selected folder
	    self.FileText.delete('1.0',Tkinter.END)

        def globSearch(self):    
            #func for get files in selected folder
            for file in glob.glob( self.DirEntry.get() ):
                print file 
                self.File.set( file + '\n' )
                self.FileText.insert(Tkinter.END,self.File.get())

	#func for get files in selected folder
	def walkFunc(self,ext,dir,files):
		goodfiles = [x for x in files if x.endswith(ext)==1]
		for goodfile in goodfiles:
			goodfile = os.path.join(dir,goodfile)
			self.File.set(goodfile+'\n')
			self.FileText.insert(Tkinter.END,self.File.get())
			
        def OsPathWalkSearch(self):    
            #func for get files in selected folder
	    os.path.walk( self.DirEntry.get(),self.walkFunc,self.Ext.get() )

	#func for SetDir button
	def setDirFunc(self):
		directory = tkFileDialog.askdirectory(title = 'Directory:')
		self.Dir.set(directory)

	#func for get batch text
	def getBatchFileContent(self):
		fileTxt = self.FileText.get('1.0',Tkinter.END)
		batchFileContent = ''
		if len(fileTxt):
			for txt in fileTxt.split('\n'):
		 		if len(txt):
			                batchFileContent += txt +'\n' 
		return batchFileContent
	#func for save to file
	def saveToBatchFileFunc(self,fileName):
		try:
			batchFileContent = self.getBatchFileContent()
			file = open(fileName,'w')
			file.write(batchFileContent)
		except IOError:
			tkMessageBox.showeror('save error...',
					      'Could not save to ',fileName)
	#func for SaveBatchFile button
	def saveBatchFileButtonFunc(self):
		batchFileName = tkFileDialog.asksaveasfilename(title = 'Save File List' )
		self.saveToBatchFileFunc(batchFileName)
                
	def Run(self):
		self.root.mainloop()
                
if (__name__=='__main__'):
	SearchFileTool().Run()
	



