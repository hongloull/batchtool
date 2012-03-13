#Description:modify image file from file lists
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.11.17
#How to use :
import os.path
import os
import sys
import string
import getopt
def imageResize(argv):
    exeFile = None
    imageSize = None
    try:
        opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
    except getopt.GetoptError:
        print ('Usage:\nimageResize -e /mnt/data/maya2008-x64/bin/imconvert -s 256 /tmp/foo.tga\n'+
               'imageResize -e /mnt/data/maya2008-x64/bin/imconvert -s 25% /tmp/foo.tga')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "-help"):
            print ('Usage:\nimageResize -e /mnt/data/maya2008-x64/bin/imconvert -s 256 /tmp/foo.tga\n'+
                   'imageResize -e /mnt/data/maya2008-x64/bin/imconvert -s 25% /tmp/foo.tga')
            sys.exit()
        elif opt in ("-e", "-exe"):
            exeFile = arg
        elif opt in ("-s","-size"):
            imageSize = arg
    goodFile = "".join(args)
    if exeFile == None :
        exeFile = 'imconvert'
    if imageSize == None :
        imageSize = '256'
    print imageSize
    #try:
    os.system( exeFile + ' ' + goodFile + ' -resize ' + imageSize + 'x' + imageSize + ' ' + goodFile )
    print( exeFile + ' ' + goodFile + ' -resize ' + imageSize + 'x' + imageSize + ' ' + goodFile )
    #except:
    #        pass
    print '\n',goodFile

if __name__ == "__main__" :
    imageResize( sys.argv[1:] )
    
