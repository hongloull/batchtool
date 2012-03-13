#Description:modify image file from file lists
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.07
#How to use :
import os.path
import os
import sys
import string
def imageConvert(fileList):    
    #func for get files in selected folder
    for file in fileList:
        try:
                os.system('cp ' + (dir+'\/'+goodfile) + ' ' + (dir+'\/'+'.'+goodfile) )
        except:
                pass
        try:
                os.system('imconvert ' + (dir+'\/'+goodfile) + ' -resize 256x256>25% ' + (dir+'\/'+goodfile) )
        except:
                pass
        goodfile = os.path.join(dir,goodfile)
        print 'goodfile=',goodfile,'\n'


