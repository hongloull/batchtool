#!/usr/bin/python
#Description:Get maya info by commandPort
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.18
#Update:2008.03.18
#How to use :
import telnetlib
def getMayaInfo():
    mayaCmd =  '\n' + 'python' + '(\"' + 'import maya.cmds as cmds' + '\");'
    mayaCmd +=  '\n' + 'python' + '(\"' + 'import maya.mel' + '\");'
    mayaCmd +=  '\n' + 'python' + '(\"' + 'mayaLoc = maya.mel.eval( \\\"getenv MAYA_LOCATION\\\" )' + '\");'
    mayaCmd +=  '\n' + 'python' + '(\"' + 'sceneName = cmds.file(q=1,sn=1)' + '\");'
    mayaCmd +=  '\n' + 'python' + '(\"' + 'print \'maya location:\',mayaLoc' + '\");'
    mayaCmd +=  '\n' + 'python' + '(\"' + 'print \'current scene:\',sceneName' + '\");'
    echo = telnetlib.Telnet('localhost',7720)
    echo.write(mayaCmd)
    echo.write('quit -f')
    print echo.read_some()

getMayaInfo()

    
