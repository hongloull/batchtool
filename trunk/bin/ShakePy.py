#!/usr/bin/env python
#Description:Batch tool for maya and operation system
#Version:1.00
#Author:honglou(hongloull@hotmail.com)
#Create:2008.01.27
#Update:2009.05.13
import re
import tempfile
import os

class ShakePy:
    def __init__(self):
        pass

    #get file content
    def getFileContent(self,fileName):
        f = open(fileName,'r')
        fileContent = f.readlines()
        f.close()
        return fileContent

    def getTimeRange(self,fileName):
        fileContent = str( self.getFileContent( fileName ) )
        #print fileContent
        p = re.compile(r'SetTimeRange\("[0-9]+-[0-9]+"\)')
        #print p.search( fileContent ).group()
        p = p.search( fileContent ).group()
        p = p.replace('SetTimeRange(\"','').replace('\")','')
        p = p.split('-')
        #print p
        return p

    def render(self,fileName):
        timeRange = self.getTimeRange( fileName )
        # render for windows
        if os.name == 'nt':
            os.system('for /l %i in (' + timeRange[0] + ',1,'+ timeRange[1] + ') do shake -exec ' + fileName + ' -vv -t %i')
        
if __name__ == '__main__':
    #Shake().render('/mnt/source/tmp/jma/test3.shk')
    import sys
    if len(sys.argv) == 2:
        ShakePy().render( sys.argv[1] )

