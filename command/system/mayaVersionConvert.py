#!/usr/bin/env python
#Description:convert ma files from high version to lower version
#Author:honglou(hongloull@hotmail.com)
#Create:2008.05.21
#Update:2008.11.21
#How to use :
import re
import sys
import tkMessageBox
import getopt

#convert ma files from high version to low version
def mayaVersionConvert(argv):
    #init version to 8.5
    ver = '8.5'
    usage = '''Usage:
mayaVersionConvert -v 8.5 mayaFile1.ma mayaFile2.ma
    '''
    try:
        opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "-help"):
            print usage
            sys.exit()
        elif opt in ("-v", "-version"):
            ver = arg
    mayaFile = "*".join(argv)
    if not mayaFile :
        print usage
        sys.exit(2)
     
    if not mayaFile :
        print 'Please get some maya files to convert\n', usage
    else:
        #get file lists
        for fileName in mayaFile.split('*'):
            print 'fileName = %s' % fileName
            try:
                f = open( fileName ,'r+' )
            except IOError:
                tkMessageBox.showerror('open error...',('Could not open '+fileName))
            else:
                #requires maya "8.5";
                patterns = {'requires maya \"\d(.)*(\d)*\";':('requires maya \"'+ver+'\";'),\
                            'fileInfo \"product\" \"Maya\s+\w+\s+\d(.)*(\d)*\";':('fileInfo \"product\" \"Maya Unlimited '+ver+'\";'),\
                            'fileInfo \"version\" \"\d(.)*(\d)*':('fileInfo \"version\" \"'+ver+'\";')}
                for pattern,repl in patterns.items():
                    f = open( fileName ,'r+' )
                    fileContent = f.read()
                    print 'pattern=%s' % pattern
                    print 'repl=%s' % repl
                    #print re.search( pattern,fileContent )
                    if re.search( pattern,fileContent ):
                        print re.search(pattern,fileContent).group()
                        #print re.sub( pattern,'requires maya \"7.0\";',fileContent )
                        f.seek(0)
                        f.write( re.sub( pattern,repl,fileContent ) )
                        f.close()

if __name__ == "__main__":
    mayaVersionConvert(sys.argv[1:])
