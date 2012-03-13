#!/usr/bin/python
#Description:Get maya info by commandPort
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.18
#Update:2008.03.18
#How to use :
import sys
sys.path.append('/mnt/data/maya8.5-x64/lib/python2.4/site-packages')

import maya.standalone
maya.standalone.initialize( )

import maya.cmds as cmds
def viewPic():
    cmds.fcheck('/mnt/production/ASP_RnD/mayaProject/images/furDuck.iff')
    
    



    
