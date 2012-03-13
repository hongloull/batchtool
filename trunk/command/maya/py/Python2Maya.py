#!/usr/bin/python
#Description:Get maya info by python mode maya.standalone
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.22
#Update:2008.04.18
#How to use :
import os

class Python2Maya:
    def __init__(self):
        #ldLibPath = os.environ['LD_LIBRARY_PATH']
        #os.environ['LD_LIBRARY_PATH'] = ldLibPath + ':/mnt/data/maya2008/lib' 
        os.putenv('MAYA_LOCATION','/mnt/data/maya2008')    
        os.putenv('PYTHONPATH','/mnt/data/maya2008/lib/python2.5/site-packages')    
        os.putenv('LD_LIBRARY_PATH','/mnt/data/maya2008/lib')     
        ## os.system( 'export MAYA_LOCATION=/mnt/data/maya2008'  )
        ## os.system( 'export PYTHONPATH=/mnt/data/maya2008/lib/python2.5/site-packages'  )
        ## os.system( 'export LD_LIBRARY_PATH=/mnt/data/maya2008/lib'  )
        print os.system('$MAYA_LOCATION')
        #print os.system('$PYTHONPATH')
        #print os.system('$LD_LIBRARY_PATH')
        import maya.standalone
        maya.standalone.initialize()
        import maya.mel
        import maya.cmds

    def getInfo(self):
        mayaLoc = maya.mel.eval("getenv MAYA_LOCATION")
        print 'Maya Location:',mayaLoc
        mayaVer = maya.cmds.about(v=1)
        print 'Maya Version:',mayaVer

    def Run(self):
       	self.getInfo()

if (__name__=='__main__'):
	Python2Maya().Run()
