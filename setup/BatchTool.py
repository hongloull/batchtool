#!/usr/bin/env python
#Description:Batch tool for maya and operation system
#Version:1.00
#Author:honglou(hongloull@hotmail.com)
#Create:2008.01.27
#Update:2009.05.13
import Tkinter,tkFileDialog,tkMessageBox,os,sys,string,re,shutil
import tempfile,traceback
import Pmw

class MyFrame(Tkinter.Frame):
	def __init__(self,root):
		Tkinter.Frame.__init__(self,root)
class MyLabel(Tkinter.Label):
	def __init__(self,root,**args):
		Tkinter.Label.__init__(self,root,**args)
	def pack(self,**args):
		if args:
			Tkinter.Label.pack(self,**args)
		else:
			Tkinter.Label.pack(self,side=Tkinter.LEFT)
class MyEntry(Tkinter.Entry):
	def __init__(self,root,width=50,**args):
		Tkinter.Entry.__init__(self,root,width=width,**args)
	def pack(self,**args):
		if args:
			Tkinter.Entry.pack(self,**args)
		else:
			Tkinter.Entry.pack(self,side=Tkinter.LEFT)
class MyButton(Tkinter.Button):
	def __init__(self,root,**args):
		Tkinter.Button.__init__(self,root,**args)
	def pack(self,**args):
		if args:
			Tkinter.Button.pack(self,**args)
		else:
			Tkinter.Button.pack(self,side=Tkinter.LEFT)
class MyScrollbar(Tkinter.Scrollbar):
	def __init__(self,root):
		Tkinter.Scrollbar.__init__(self,root)
	def pack(self,**args):
		if args:
			Tkinter.Scrollbar.pack(self,**args)
		else:
			Tkinter.Scrollbar.pack(self,side = Tkinter.RIGHT,fill = Tkinter.Y)
class MyText(Tkinter.Text):
	def __init__(self,root,height=25,**args):
		Tkinter.Text.__init__(self,root,height=height,**args)
	def pack(self,**args):
		if args:
			Tkinter.Text.pack(self,**args)
		else:
			Tkinter.Text.pack(self,side = Tkinter.LEFT)		

class BatchTool:
	'''
I.   What is the Batch Tool?
     The Batch Tool is a tool kit to do Maya rendering and batch processing for large amount of files. It serves as a bridge between Maya, operating system and local area network.
     The Batch Tool allows you to:
     *)Do Maya network rendering.
     *)Do batch processing on Maya files, such as the absolute and relative path conversion for file texture.
     *)Do batch processing on operating system files, such as the format and resolution conversion for image files.
     *)Do batch processing on local area network files.
II.  How to install and run the Batch Tool?
     *)Windows system
     Unzip the BathTool.rar and directly run BatchTool.exe and NetRenderServer.exe in the BIN directory.
     *)Linux system
     Python and its Tkinter module are required for the Batch Tool installation.
     Unzip the BathTool.rar and run the following on the terminal:
      cd /yourFolderFullPath/BatchTool/bin
      python NetRenderServer.pyc
      python BatchTool.pyc
III.  Both the English and the Chinese version tutorial files can be found in the BatchTool.rar archive.
        '''
	def __init__(self):
		#def attribute
		self.preferenceEntry = {}
		self.preferenceMayaEntry = {}
		#def the dictionary of batch tool for maya's env
		#For nt, repalce '\' with '/'
		curDir = os.getcwd().replace('\\','/')
		self.BatchToolDir = re.search('^.*/',curDir).group()
		# check and create usr batchTool dir
		self.createUserSettingsFile()
		#get the env dictionary
		self.env = {}
		self.getEnv('batchTool')
		self.envMaya = {}
		self.getEnvMaya('maya')
		#create GUI window
		self.CreateWidgets()
		#
		self.hostsFlag = {}
		self.HostSetFlag = {}
		self.tmp = ''
		self.cmdDict = {}
		self.logDict = {}
                
	def CreateWidgets(self):
		self.root = Tkinter.Tk()
		self.root.title('Batch Tools V1.0')
		self.BatchConfig = Tkinter.IntVar()
		self.BatchConfig.set(0)
		self.MayaBatchVar = Tkinter.IntVar()
		self.MayaBatchVar.set(0)
		self.PowerOffAfterBatch = Tkinter.IntVar()
		self.PowerOffAfterBatch.set(0)
		self.File = Tkinter.StringVar()
		self.CommandMaya = Tkinter.StringVar()
		#var for render farm control
		self.StartFrameEntryVar = Tkinter.StringVar()
		self.EndFrameEntryVar = Tkinter.StringVar()
		self.ByFrameEntryVar = Tkinter.StringVar()
		self.FramesPerServerEntryVar = Tkinter.StringVar()

		#Create the menu
		Menu = Tkinter.Menu(self.root)
		#Create the File menu
		FileSubMenu = Tkinter.Menu(Menu,tearoff=0)
		FileSubMenu.add_command( label='Open File',command=self.openFile )
		FileSubMenu.add_command( label='Open Directory',command=self.openDirectory )
		FileSubMenu.add_separator()
		#FileSubMenu.add_command( label='Open Batch File',command=self.openBatchFileButtonFunc )
		#FileSubMenu.add_command( label='Save Batch File',command=self.saveBatchFileButtonFunc )
		FileSubMenu.add_command( label='Exit',command=sys.exit )
		Menu.add_cascade(label='File',menu=FileSubMenu)

		#Create the Edit menu
		FileSubMenu = Tkinter.Menu(Menu,tearoff=0)
		#FileSubMenu.add_command( label='Load Preferences',command=self.loadPreference )
		FileSubMenu.add_command( label='Preferences',command=self.createPreferenceWin )
		FileSubMenu.add_command( label='Maya Preferences',command=self.createMayaPreferenceWin )
		Menu.add_cascade(label='Edit',menu=FileSubMenu)

## 		#Config Frame for maya or system settings
## 		ConfigFrame = MyFrame(self.root)
## 		ConfigFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)
## 		ConfigLabel = MyLabel(ConfigFrame,width=18,text='Sort:').pack()
## 		for batchType,batchVal in [('Maya',0),('System',1)]:
## 			ConfigRadBtn = Tkinter.Radiobutton( ConfigFrame,
## 							    text=batchType,
## 							    value=batchVal,
## 							    variable=self.BatchConfig )
## 			ConfigRadBtn.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)


		#file list label Frame
		#FileListFrame = MyFrame(self.root)
		#FileListFrame.pack()
		#FileListLabel = MyLabel(FileListFrame,text='File List:').pack()
		#file Frame
		FileFrame = Tkinter.Frame(self.root)
		FileFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)

		# Create and pack the NoteBook.
		notebook = Pmw.NoteBook( FileFrame )
		notebook.pack(fill = 'both', expand = 1, padx = 1, pady = 1)
		# Add the "File" page to the notebook.
		filePage = notebook.add('File')
		notebook.tab('File').focus_set()
		# Create the "File List" contents of the page.
		fileGroup = Pmw.Group(filePage, tag_text = 'File Lists:')
		fileGroup.pack(fill = 'both', expand = 1, padx = 1, pady = 1)
		FileScrollbar = MyScrollbar( fileGroup.interior() )
		FileScrollbar.pack()
		self.FileText = MyText(fileGroup.interior(),yscrollcommand=FileScrollbar.set,height=15)
		self.FileText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		FileScrollbar.config(command=self.FileText.yview)
		
		# Add the "maya command" page to the notebook.
		mayaCmdPage = notebook.add('Maya Command')
		# Create the "File List" contents of the page.
		mayaCmdGroup = Pmw.Group(mayaCmdPage, tag_text = 'Maya Command Lists:')
		mayaCmdGroup.pack(fill = 'both', expand = 1, padx = 1, pady = 1)
		
		# maya cmd settings
		MayaCmdFrame = MyFrame( mayaCmdGroup.interior() )
		MayaCmdFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)
		MayaCmdLabel = MyLabel(MayaCmdFrame,width=18,text='Batch:').pack()
		for batchType,batchVal in [('Yes',1),('No',0)]:
			MayaCmdRadBtn = Tkinter.Radiobutton( MayaCmdFrame,
							     text=batchType,
							     value=batchVal,
							     variable=self.MayaBatchVar )
			MayaCmdRadBtn.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)		
		CmdMayaScrollbar = MyScrollbar( mayaCmdGroup.interior() )
		CmdMayaScrollbar.pack()
		self.CmdMayaText = MyText(mayaCmdGroup.interior(),yscrollcommand=CmdMayaScrollbar.set,height=15)
		CmdMayaScrollbar.config(command=self.CmdMayaText.yview)
		self.CmdMayaText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		
		#create default maya command
		#read command from env's default command
                if self.envMaya.get('mayaDefaultCommand') != None:
			self.CmdMayaText.insert( Tkinter.END,(self.envMaya.get('mayaDefaultCommand') + '\n') )
	
		sysCmdPage = notebook.add('System Command')
		# Create the "sys command" contents of the page.
		sysCmdGroup = Pmw.Group(sysCmdPage, tag_text = 'System Command Lists:')
		sysCmdGroup.pack(fill = 'both', expand = 1, padx = 1, pady = 1)
		#system python command Frame
		#Config Frame for system settings :poweroff
		ConfigOtherFrame = MyFrame(sysCmdGroup.interior())
		ConfigOtherFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)
		ConfigOtherLabel = MyLabel(ConfigOtherFrame,width=18,text='Power Off:').pack()
		for batchType,batchVal in [('Yes',1),('No',0)]:
			ConfigOtherRadBtn = Tkinter.Radiobutton( ConfigOtherFrame,
								 text=batchType,
								 value=batchVal,
								 variable=self.PowerOffAfterBatch )
			ConfigOtherRadBtn.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
			
		CmdSysScrollbar = MyScrollbar( sysCmdGroup.interior() )
		CmdSysScrollbar.pack()
		self.CmdSysText = MyText(sysCmdGroup.interior(),yscrollcommand=CmdSysScrollbar.set,height=15)
		self.CmdSysText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		CmdSysScrollbar.config(command=self.CmdSysText.yview)		
		#read command from env's default command
                if self.env.get('systemDefaultCommand') != None:
			self.CmdSysText.insert( Tkinter.END,(self.env.get('systemDefaultCommand') + '\n') )

		# Add the "File" page to the notebook.
		batFilePage = notebook.add('Batch File')
		# Create the "File List" contents of the page.
		batFileGroup = Pmw.Group(batFilePage, tag_text = 'Batch File:')
		batFileGroup.pack(fill = 'both', expand = 1, padx = 1, pady = 1)
		BatFileScrollbar = MyScrollbar( batFileGroup.interior() )
		BatFileScrollbar.pack()
		self.BatFileText = MyText(batFileGroup.interior(),yscrollcommand=BatFileScrollbar.set,height=15)
		self.BatFileText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		BatFileScrollbar.config(command=self.BatFileText.yview)
		
## 		#use Toplevel widget to create the preference window
## 		self.batFileRoot = Tkinter.Toplevel(self.root)
## 		self.batFileRoot.title('Batch File')
## 		#system python command Frame
## 		batFileFrame = MyFrame(self.batFileRoot)
## 		batFileFrame.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
## 		batFileScrollbar = MyScrollbar(batFileFrame)
## 		batFileScrollbar.pack()
## 		self.batFileText = MyText(batFileFrame,yscrollcommand=batFileScrollbar.set,height=25)
## 		self.batFileText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
## 		batFileScrollbar.config(command=self.batFileText.yview)		
## 		#add batch file content to widget
## 		self.batFileText.insert( Tkinter.END, self.getBatchFileContent() )
## 		#batch file Frame
## 		BatchFileFrame1 = MyFrame(self.batFileRoot)
## 		BatchFileFrame1.pack()
## 		OpenBatchFileButton = MyButton(BatchFileFrame1,text='Open',width=20,
## 						  command=self.openBatchFileButtonFunc)
## 		OpenBatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
## 		SaveBatchFileButton = MyButton(BatchFileFrame1,text='Save',width=20,
## 					   command=self.saveBatchFile)
## 		SaveBatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		
		notebook.setnaturalsize()
		
		#batch file Frame
		BatchFileFrame = MyFrame(self.root).pack()
		PreviewBatchFileButton = MyButton(BatchFileFrame,text='View Batch File',width=18,
						  command=self.viewBatchFile)
		PreviewBatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		Append2BatchFileButton = MyButton(BatchFileFrame,text='Append to Batch File',width=18,
						  command=self.append2BatchFile)
		Append2BatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		BatchFileButton = MyButton(BatchFileFrame,text='Save Batch File',width=18,command=self.saveBatchFileButtonFunc)
		BatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		StartBatchButton = MyButton(BatchFileFrame,text='Start Batch',width=18,command=self.startBatchButtonFunc)
		StartBatchButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		exitBatchButton = MyButton(BatchFileFrame,text='  Exit  ',width=18,command=sys.exit)
		exitBatchButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)	

                #Create the Command menu for 'mel' dir
		MelSubMenu = Tkinter.Menu(Menu,tearoff=0)
		MelSubMenu.add_command( label='Source Mel',command = self.sourceMel )
		MelSubMenu.add_separator()
		MelSubMenu.add_command( label='Batch Render',command = self.batchRenderFunc )
		MelSubMenu.add_separator()
		melFiles = os.listdir(  os.path.normpath( self.BatchToolDir+'command/maya/mel') )
		for x in melFiles :
			if x.endswith('.mel') :
				cmd = self.BatchToolDir+'command/maya/mel/'+x
				subMenu = MelSubMenu.add_command( label=re.sub(r'(.mel)$','',x),
								  command=lambda f=cmd:self.sourceMel(f) )
		Menu.add_cascade(label='Mel',menu=MelSubMenu)

                #create the Command menu for 'py' dir
		PySubMenu = Tkinter.Menu(Menu,tearoff=0)
		PySubMenu.add_command( label='Source Py',command = self.sourcePy )
		PySubMenu.add_separator()
		for x in os.listdir( os.path.normpath(self.BatchToolDir+'command/maya/py') ) :
			if x.endswith('.py') :
				if x!= '__init__.py' and x[-1]!='~':
					if x.endswith('.pyc') :
						pass
					else :
						cmd = self.BatchToolDir+'command/maya/py/'+x
						subMenu = PySubMenu.add_command( label=re.sub(r'(.py)$','',x),
										 command=lambda f=cmd:self.sourcePy(f) )
		Menu.add_cascade(label='Py',menu=PySubMenu)
		
                #Create the Command menu for 'python' dir
		PySubMenu = Tkinter.Menu(Menu,tearoff=0)
		PySubMenu.add_command( label='Source Python',command = self.sysPython )
		PySubMenu.add_separator()
		PySubMenu.add_command( label='Shake Render',command = self.shake )
		PySubMenu.add_separator()
		for x in os.listdir( os.path.normpath(self.BatchToolDir+'command/system') ) :
			if x.endswith('.py') :
				if x!= '__init__.py':
					cmd = self.BatchToolDir+'command/system/'+x
					subMenu = PySubMenu.add_command( label=re.sub(r'(.py)$','',x),
									 command=lambda f=cmd:self.sysPython(f) )
		Menu.add_cascade(label='Python',menu=PySubMenu)  		

		#Create the Render Farm menu
		RFMenu = Tkinter.Menu(Menu,tearoff=0)
		RFMenu.add_command( label='Net Render',command = self.netRenderFunc )
## 	        HuntGroupMenu = Tkinter.Menu( RFMenu,tearoff=0 )
## 		HuntGroupMenu.add_command( label='Master Schedule' )
##		RFMenu.add_cascade( label='Huntgroup...',menu=HuntGroupMenu )
		Menu.add_cascade( label='Render Farm',menu=RFMenu )
		
		#Create the Help menu
		HelpMenu = Tkinter.Menu(Menu,tearoff=0)
		HelpMenu.add_command(label='Help',command=self.helpFunc)
		HelpMenu.add_command(label='About',command=self.aboutFunc)
		Menu.add_cascade(label='Help',menu=HelpMenu)
		self.root.config(menu=Menu)

	##############################################
	#Function
	##############################################
	#get config info from *./etc/batchTool.env
	def getEnv( self,confFile ):
		fileName = []
		# There are two env files one for nt and the other for linux
		if os.name == 'posix':
			fileName.append ( self.UserBatchToolDir + 'etc/' + confFile +'_Linux.env' )
		else:
			fileName.append ( self.UserBatchToolDir + 'etc/' + confFile + '_Nt.env' )
		for f in fileName:
			try:
				f = open( f ,'r' )
			except IOError:
				tkMessageBox.showerror('open error...',('Could not open '+f))
			else:
				for x in f.readlines():
					self.env[ x.strip().split('=')[0] ] = x.strip().split('=')[1]
				f.close()
		return self.env

	def getEnvMaya( self,confFile ):
		fileName = []
		# There are two env files one for nt and the other for linux
		if os.name == 'posix':
			fileName.append ( self.UserBatchToolDir + 'etc/' + confFile +'_Linux.env' )
		else:
			fileName.append ( self.UserBatchToolDir + 'etc/' + confFile + '_Nt.env' )
		for f in fileName:
			try:
				f = open( f ,'r' )
			except IOError:
				tkMessageBox.showerror('open error...',('Could not open '+f))
			else:
				for x in f.readlines():
					self.envMaya[ x.strip().split('=')[0] ] = x.strip().split('=')[1]
				f.close()
		return self.envMaya

	def createUserSettingsFile(self):
		# get user home dir
		self.UserBatchToolDir = os.path.expanduser('~') + '/BatchTool/' 
		if not os.path.exists( self.UserBatchToolDir ):
			os.makedirs( self.UserBatchToolDir + 'etc' )
			# copy etc files to user dir
			for f in os.listdir( (self.BatchToolDir + 'etc') ):
				if os.path.isfile( (self.BatchToolDir + 'etc/' + f) ):
					shutil.copy( (self.BatchToolDir + 'etc/' + f), (self.UserBatchToolDir + 'etc/') )
		
	def createPreferenceWin(self):
		#use Toplevel widget to create the preference window
		self.preferenceRoot = Tkinter.Toplevel(self.root)
		self.preferenceRoot.title('Batch Tools\'s Preference Setting')
		#create preference widget from self.env
		for x in self.env.keys():
			ConfigureFrame = MyFrame(self.preferenceRoot)
			MyLabel(ConfigureFrame,width=25,text=(x+':').rjust(25) ).pack(side=Tkinter.LEFT)
			optEntry = MyEntry(ConfigureFrame,width=50 )
			optEntry.insert( 0,self.env[x] )
			#bind func for preference entry
			optEntry.bind( '<Enter>',lambda event,pre=x:self.setPreferenceOptionEntryFunc(event,pre) )
			optEntry.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
			#write preference entry'name to self.preferenceEntry for bind func use
			self.preferenceEntry[x] = optEntry 
			#if value is a dir options ,then add 'set' button
			if self.env[x].find('/') != -1:
				#use lambda def for transform args
				self.prefButton = MyButton( ConfigureFrame,text='Set',width=10,
							    command=(lambda pre=x:self.setPreferenceOptionButtonFunc(pre)) )
				self.prefButton.pack()
			#add label widget for align with button widget
			else:
				MyLabel(ConfigureFrame,width=10).pack()
			ConfigureFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)
		#save preference Frame
		PreferenceFrame = MyFrame(self.preferenceRoot)
		PreferenceFrame.pack()
		SavePreferenceButton = MyButton( PreferenceFrame,
						 text='Save Preferences To File',width=25,
						 command=self.savePreference ).pack()
		
	def createMayaPreferenceWin(self):
		#use Toplevel widget to create the preference window
		self.preferenceMayaRoot = Tkinter.Toplevel(self.root)
		self.preferenceMayaRoot.title('Batch Tools\'s Preference Setting')
		#create preference widget from self.envMaya
		for x in self.envMaya.keys():
			ConfigureFrame = MyFrame(self.preferenceMayaRoot)
			MyLabel(ConfigureFrame,width=25,text=(x+':').rjust(25) ).pack(side=Tkinter.LEFT)
			optEntry = MyEntry(ConfigureFrame,width=50 )
			optEntry.insert( 0,self.envMaya[x] )
			#bind func for preference entry
			optEntry.bind( '<Enter>',lambda event,pre=x:self.setMayaPreferenceOptionEntryFunc(event,pre) )
			optEntry.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
			#write preference entry'name to self.preferenceEntry for bind func use
			self.preferenceMayaEntry[x] = optEntry 
			#if value is a dir options ,then add 'set' button
			if self.envMaya[x].find('/') != -1:
				#use lambda def for transform args
				self.prefButton = MyButton( ConfigureFrame,text='Set',width=10,
							    command=(lambda pre=x:self.setMayaPreferenceOptionButtonFunc(pre)) )
				self.prefButton.pack()
			#add label widget for align with button widget
			else:
				MyLabel(ConfigureFrame,width=10).pack()
			ConfigureFrame.pack(expand=Tkinter.YES,fill=Tkinter.X)
		#save preference Frame
		PreferenceFrame = MyFrame(self.preferenceMayaRoot)
		PreferenceFrame.pack()
		SavePreferenceButton = MyButton( PreferenceFrame,
						 text='Save Maya Preferences To File',width=25,
						 command=self.saveMayaPreference ).pack()

	def viewBatchFile(self):
		#use Toplevel widget to create the preference window
		self.batFileRoot = Tkinter.Toplevel(self.root)
		self.batFileRoot.title('Batch File')
		#system python command Frame
		batFileFrame = MyFrame(self.batFileRoot)
		batFileFrame.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
		batFileScrollbar = MyScrollbar(batFileFrame)
		batFileScrollbar.pack()
		self.batFileText = MyText(batFileFrame,yscrollcommand=batFileScrollbar.set,height=25)
		self.batFileText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		batFileScrollbar.config(command=self.batFileText.yview)		
		#add batch file content to widget
		self.batFileText.insert( Tkinter.END, self.getBatchFileContent() )
		#batch file Frame
		BatchFileFrame1 = MyFrame(self.batFileRoot)
		BatchFileFrame1.pack()
		OpenBatchFileButton = MyButton(BatchFileFrame1,text='Open',width=20,
						  command=self.openBatchFileButtonFunc)
		OpenBatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		SaveBatchFileButton = MyButton(BatchFileFrame1,text='Save',width=20,
					   command=self.saveBatchFile)
		SaveBatchFileButton.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)

	def aboutFunc(self):
		#use Toplevel widget to create the preference window
		self.aboutRoot = Tkinter.Toplevel(self.root)
		self.aboutRoot.title('BatchTool Info')
		#system python command Frame
		aboutFrame = MyFrame(self.aboutRoot)
		aboutFrame.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
		aboutScrollbar = MyScrollbar(aboutFrame)
		aboutScrollbar.pack()
		self.aboutText = MyText(aboutFrame,yscrollcommand=aboutScrollbar.set,height=8)
		self.aboutText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		aboutScrollbar.config(command=self.aboutText.yview)
		#about str
		aboutStr = '''
		Description:Batch tool for maya and operation system
		Version:1.00
		Author:honglou
		Mail:hongloull@hotmail.com
		Create:2008.01.27
		Update:2008.12.27
		'''
		self.aboutText.insert( Tkinter.END, aboutStr )

	def helpFunc(self):
		#use Toplevel widget to create the preference window
		self.helpRoot = Tkinter.Toplevel(self.root)
		self.helpRoot.title('Batch Tool Help')
		#system python command Frame
		helpFrame = MyFrame(self.helpRoot)
		helpFrame.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
		helpScrollbar = MyScrollbar(helpFrame)
		helpScrollbar.pack()
		self.helpText = MyText(helpFrame,yscrollcommand=helpScrollbar.set,height=40)
		self.helpText.pack(side=Tkinter.LEFT,expand=Tkinter.YES,fill=Tkinter.X)
		helpScrollbar.config(command=self.helpText.yview)
		#help str
		helpStr = self.__doc__
		self.helpText.insert( Tkinter.END, helpStr )
		
	#func for preference entry
	def setPreferenceOptionEntryFunc(self,event,preference):
		self.env[preference] = self.preferenceEntry[preference].get()	      

	#func for preference button
	def setPreferenceOptionButtonFunc(self,preference):
		dirName = tkFileDialog.askdirectory(title = 'Set Preference',
						    initialdir=self.env.get(preference) )
		self.env[preference] = dirName
		self.preferenceEntry[preference].delete(0,Tkinter.END)
		self.preferenceEntry[preference].insert( 0,self.env[preference] )
		
	#func for preference entry
	def setMayaPreferenceOptionEntryFunc(self,event,preference):
		self.envMaya[preference] = self.preferenceMayaEntry[preference].get()	      

	#func for preference button
	def setMayaPreferenceOptionButtonFunc(self,preference):
		dirName = tkFileDialog.askdirectory(title = 'Set Preference',
						    initialdir=self.envMaya.get(preference) )
		self.envMaya[preference] = dirName
		self.preferenceMayaEntry[preference].delete(0,Tkinter.END)
		self.preferenceMayaEntry[preference].insert( 0,self.envMaya[preference] )
		
        #func for save preferences
	def savePreference(self):
		#Linux
		if os.name == 'posix':
			refFile = 'batchTool_Linux.env'
		#Windows
		else:
			refFile = 'batchTool_Nt.env'
		try:
			# get etc file from user batchtool dir
			#f = open( ( self.BatchToolDir + 'etc/' + refFile ),'w' )
			f = open( ( self.UserBatchToolDir + 'etc/' + refFile ),'w' )
		except IOError:
			tkMessageBox.showerror('save error...',('Could not save to '+f) )
		else:
			fContent = ''
			for x in self.env.keys():
				if self.preferenceEntry[x].get():
				#print self.preferenceEntry[i]
					self.env[x] = self.preferenceEntry[x].get().splitlines()[0]
					#print (x+':').rjust(30), self.preferenceEntry[i].get(),'\n'
					fContent +=  x + '=' + self.preferenceEntry[x].get().splitlines()[0] + '\n'
				else :
					fContent +=  x + '=' + '' + '\n'
			f.write(fContent)
			f.close()
			#close save preference window
			self.preferenceRoot.destroy()
		
        #func for save preferences
	def saveMayaPreference(self):
		#Linux
		if os.name == 'posix':
			refFile = 'maya_Linux.env'
		#Windows
		else:
			refFile = 'maya_Nt.env'
		try:
			f = open( ( self.UserBatchToolDir + 'etc/' + refFile ),'w' )
		except IOError:
			tkMessageBox.showerror('save error...',('Could not save to '+f) )
		else:
			fContent = ''
			for x in self.envMaya.keys():
				#print self.preferenceEntry[i]
				if self.preferenceMayaEntry[x].get():
					self.envMaya[x] = self.preferenceMayaEntry[x].get().splitlines()[0]
					#print (x+':').rjust(30), self.preferenceEntry[i].get(),'\n'
					fContent +=  x + '=' + self.preferenceMayaEntry[x].get().splitlines()[0] + '\n'
					#print fContent
				else:
					fContent +=  x + '=' + '' + '\n'
			f.write(fContent)
			f.close()
			#close save preference window
			self.preferenceMayaRoot.destroy()

	#func for net render
	def netRenderFunc(self):
		pass
	
        #func for load preferences
	def loadPreference(self):
		f = tkFileDialog.askopenfilename( title = 'Open File',initialdir = (self.BatchToolDir + 'config'),
						  filetypes=[('All files','*')] )
		if len(f):
			self.getEnv( f )
			
	#get file content
	def getFileContent(self,fileName):
		f = open(fileName,'r')
		fileContent = f.readlines()
		f.close()
		return fileContent
	
	#set command list
	def setCommand(self,cmd):
		self.CommandMaya.set(cmd+'\n')
		self.CmdMayaText.insert( Tkinter.END,self.CommandMaya.get() )

	#func for SetProject button
	def openDirectoryInitialDirFunc(self):
		openDirectoryInitialDir = tkFileDialog.askdirectory(title = 'openDirectoryInitialDir',
						    initialdir=self.env.get('openDirectoryInitialDir') )
		self.OpenDirectoryInitialDir.set(openDirectoryInitialDir)

	#func for get files in selected folder
	def getFileInDir(self,exts,dir,files):
		#print 'dir=',dir,'files=',files
		for ext in exts:
			goodfiles = [x for x in files if x.endswith(ext)==1]
			#print 'goodfiles=',goodfiles,'\n'
			for goodfile in goodfiles:
				goodfile = os.path.join(dir,goodfile)
				#print 'goodfile=',goodfile,'\n'
				self.File.set(goodfile+'\n')
				self.FileText.insert(Tkinter.END,self.File.get())
				
	#func for get files in selected folder
	def getRFileInDir(self,exts,dir,files):
		#print 'dir=',dir,'files=',files
		for ext in exts:
			goodfiles = [x for x in files if x.endswith(ext)==1]
			#print 'goodfiles=',goodfiles,'\n'
			for goodfile in goodfiles:
				goodfile = os.path.join(dir,goodfile)
				# add items to dict	
				self.RFileList.insert(Tkinter.END,goodfile)
				# select new item
				self.selectNewRFileItem( Tkinter.END )

	#func for open file menu
	def openFile(self):
		f = tkFileDialog.askopenfilename(title = 'Open File',
						    initialdir=self.env.get('openFileInitialDir'),
						    filetypes=[('maya','*.mb *.ma *.shk'),
							       ('maya binary','*.mb'),
							       ('maya asii','*.ma'),
							       ('All files','*')] )
		if len(f):
			self.FileText.insert(Tkinter.END,(f+'\n') )

	#func for open render farm file menu
	def openRFFile(self):
		f = tkFileDialog.askopenfilename(title = 'Open File',
						    initialdir=self.env.get('openFileInitialDir'),
						    filetypes=[('maya','*.mb *.ma *.shk'),
							       ('maya binary','*.mb'),
							       ('maya asii','*.ma'),
							       ('All files','*')] )
		if len(f):
			# add items to dict
			self.RFileList.insert(Tkinter.END,f)
			# select new item
			self.selectNewRFileItem( Tkinter.END )
		
	#func for source mel
	def sourceMel(self,*args):
		if args:
			f = args[0]
		else:
			f = tkFileDialog.askopenfilename( title = 'Source Mel',
							  initialdir=self.env.get('sourceScriptInitialDir'),
							  filetypes=[('Mel','*.mel'),('All files','*')] )
		#self.File.set(file+'\n')
		if len(f):
			f = 'source ' + '\"' + f + '\";'
			self.CmdMayaText.insert( Tkinter.END,(f + '\n') )

	#func for source py
	def sourcePy(self,*args):
		if args:
			f = args[0]
		else:
			f = tkFileDialog.askopenfilename( title = 'Source Py',
							  initialdir=self.env.get('sourceScriptInitialDir'),
							  filetypes=[('Py','*.py'),('All files','*')] )
		#self.File.set(file+'\n')
		if len(f):
			f = 'python("import sys");\n' +\
			    'python("sys.path.append(\\\\"' + os.path.dirname(f) +'\\\\")");\n' +\
			    'python("import ' + os.path.splitext( os.path.basename(f) )[0] + '");\n' +\
			    'python("' + os.path.splitext(  os.path.basename(f) )[0] + '.' +\
			    os.path.splitext(  os.path.basename(f) )[0]  + '()");\n'
			self.CmdMayaText.insert( Tkinter.END,(f + '\n') )
			
	#func for source system python 
	def sysPython(self,*args):
		if args:
			f = args[0]
		else:
			f = tkFileDialog.askopenfilename( title = 'Source Python Script',
							  initialdir=self.env.get('sourcePythonInitialDir'),
							  filetypes=[('Python','*.py'),('All files','*')] )
		#self.File.set(file+'\n')
		if len(f):
			f = 'python ' + '\"' + f + '\"'
			self.CmdSysText.insert( Tkinter.END,(f+' $f ' + '\n') )	
		
	#func for for open directory menu
	def openDirectory(self):
		folder = tkFileDialog.askdirectory(title = 'Open Directory',
						   initialdir=self.env.get('openDirectoryInitialDir') )
		if len(folder)!=0:
			os.path.walk( folder,self.getFileInDir,self.env.get('openDirectoryInitialExt') )

	#func for for open directory menu
	def openRDirectory(self):
		folder = tkFileDialog.askdirectory(title = 'Open Directory',
						   initialdir=self.env.get('openDirectoryInitialDir') )
		if len(folder)!=0:
			os.path.walk( folder,self.getRFileInDir,self.env.get('openDirectoryInitialExt') )
						
	#func for rendering
	def batchRenderFunc(self):
		#write 'Render' to maya command lists
		self.CmdMayaText.insert( Tkinter.END,('BatchRender' + '\n') )

	#func for rendering
	def shake(self):
		#write 'Render' to system command lists
		#self.CmdSysText.insert( Tkinter.END,('shake -exec $f' + '\n') )
		self.CmdSysText.insert( Tkinter.END,('ShakePy.exe $f\n') )
		
	#func for get file list
	def getFileList(self):
		files = []
		#Get file lists
		fileTxt = self.FileText.get('1.0',Tkinter.END)
		if len(fileTxt):
			for fileName in fileTxt.split('\n'):
				if len(fileName):
					files.append(fileName)
		return files
	
	#func for get maya batch text
	def getBatchFileContent(self):
		batchFileContent = ''
		cmdMaya = self.CmdMayaText.get('1.0',Tkinter.END).split()
		cmdSys = self.CmdSysText.get('1.0',Tkinter.END).split()
		if cmdMaya:
			#Get mayabatch location
			mayaCmd = self.envMaya['MayaLoc']
			#For batch render
			if cmdMaya.count( 'BatchRender' ) >= 1:
				#mayaCmd += '/bin/Render' + ' -proj ' + self.envMaya['Proj']
				#Linux
				if os.name == 'posix':
					mayaCmd += '/bin/Render'
				#Windows
				else:
					mayaCmd += '/bin/Render.exe'
				mayaCmd = mayaCmd + ' -r file'
				#Get project
				cmdTxt = ' -proj ' + '\"' + self.envMaya['Proj'] + '\" '
			#For normal batch commands
			else:
				#Linux
				if os.name == 'posix':
					# start maya normal with UI
					mayaCmd = '"' + mayaCmd + '/bin/maya"' 
					# batch mode no UI
					if self.MayaBatchVar.get() == 1 :
						mayaCmd += ' -batch'
				#Windows
				else:
					# batch mode no UI
					mayaCmd = mayaCmd + '/bin/maya'
					# start maya normal with UI
					if self.MayaBatchVar.get() == 1 :
						mayaCmd += 'batch'
				#Get project
				cmdTxt = ' -proj ' + '\"' + self.envMaya['Proj'] + '\"'
				#Get command
				cmdTxt += ' -command ' + '\"' + self.CmdMayaText.get('1.0',Tkinter.END).replace('\"','\\"') + ';quit -force\"'
			
		if cmdSys:
			#get system command
			sysCmd = self.CmdSysText.get('1.0',Tkinter.END)

		#Get file lists
		fileTxt = self.FileText.get('1.0',Tkinter.END)
		
		if len(fileTxt):
			for fileName in fileTxt.split('\n'):
				if len(fileName):
					#add maya command
					if cmdMaya:
						#print  cmdMaya
						#print  cmdMaya.count( 'BatchRender' )
						if cmdMaya.count( 'BatchRender' ) >= 1:
							txtMaya = string.replace( (cmdTxt + '\"' + fileName + '\"'),'\n','' )
						else:
							txtMaya = string.replace( (cmdTxt + ' -file ' + '\"' + fileName + '\"'),'\n','' )
						batchFileContent += '\n' + mayaCmd + txtMaya
					#add system command
					if cmdSys:
						#replace the '$f' with the file
						batchFileContent += '\n' + sysCmd.replace( '$f',fileName )
		#print 'self.PowerOffAfterBatch:%s' % self.PowerOffAfterBatch.get()
		if self.PowerOffAfterBatch.get() == 1 :
			if os.name == 'posix':
				batchFileContent += '\n' + 'poweroff'
			else:
				batchFileContent += '\n' + 'shutdown -s'
		return batchFileContent
	
	#func for save to file
	def saveToBatchFileFunc(self,fileName):
		batchFileContent = self.getBatchFileContent()
		try:
			f = open(fileName,'w')
		except IOError:
			tkMessageBox.showerror('save error...',('Could not save to '+fileName) )
		else:
			f.write(batchFileContent)
			#chmod file
			if os.name == 'posix':
				os.system('chmod 777 '+fileName)
			f.close()
			
	#func for SaveBatchFile 
	def saveBatchFileButtonFunc(self):
		batchFileName = tkFileDialog.asksaveasfilename(title = 'Save Batch File',
							       initialdir=self.env.get('batchFileInitialDir'),
							       initialfile=self.env.get('batchFileInitialName') )
		self.saveToBatchFileFunc(batchFileName)

	#func for Save Batch File 
	def saveBatchFile(self):
		fileName = tkFileDialog.asksaveasfilename(title = 'Save Batch File',
							  initialdir=self.env.get('batchFileInitialDir'),
							  initialfile=self.env.get('batchFileInitialName') )
		batchFileContent = self.batFileText.get('1.0',Tkinter.END)
		try:
			f = open(fileName,'w')
		except IOError:
			tkMessageBox.showerror('save error...',('Could not save to '+fileName) )
		else:
			f.write(batchFileContent)
			#chmod file
			if os.name == 'posix':
				os.system('chmod 777 '+fileName)
			f.close()

	#func for Save Batch File 
	def append2BatchFile(self):
		batchFileContent = self.getBatchFileContent()
		self.batFileText.insert(Tkinter.END,batchFileContent)
			
	#func for open batch file 
	def openBatchFileButtonFunc(self):
		fileName = tkFileDialog.askopenfilename(title = 'Open Batch File',
							initialdir=self.env.get('batchFileInitialDir'),
							initialfile=self.env.get('batchFileInitialName') )
		try:
             		f = open( fileName ,'r' )
		except IOError:
 			tkMessageBox.showerror('open error...',('Could not open '+fileName))
		else:
			fileContent = ''
			for x in f.readlines():
				fileContent += x 
			f.close()
			self.batFileText.insert( Tkinter.END, fileContent )
		
	#func for SaveBatchFile button
	def startBatchButtonFunc(self):
		#maybe mayaCmd is larger ,os.system can not execute it,so 
		#write mayacmd to tempfile and execute this bat file
		f = tempfile.mkstemp(suffix='.bat',prefix='batchToolCmd')
		os.close(f[0])
		fObj = open(f[1],'w')
		fObj.write( self.getBatchFileContent() )
		fObj.flush()
		fObj.close()
		if os.name == 'posix' :
			os.system('chmod -R 777 ' + f[1])
		os.system(f[1])
	    
	def Run(self):
		# Start up a thread to process messages
                #host = socket.gethostbyname( socket.gethostname() )
		#port = 10061
		#threading.Thread( target=self.netRenderClientReceiveThread,args=(host,port) ).start()
		#threading.Thread( target=self.root.mainloop() ).start()
		self.root.mainloop()

if (__name__=='__main__'):
	BatchTool().Run()
