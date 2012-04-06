#Description:modify image f from f lists
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.07
#How to use :
import os.path
import os
import sys
import string
import traceback

def imageConvert(fileName):
    fd = open(fileName,'r')
    for f in fd:
        f=f.split('\n')[0]
        print f
        try:
            if f.endswith('.tga') or f.endswith('.TGA'):
                #f1 = os.path.dirname(f) + '/' + os.path.basename(f).split('.')[0]+'.tif'
                f1 = os.path.dirname(f) + '/' + os.path.basename(f).split('.')[0]+'.jpg'
                #print f1
                cmd = 'imconvert ' + f + ' -resize 2048x2048>50% -quality 100 ' + f1
                #print cmd
                os.system( cmd )
            else:
                print 'not tga'
                cmd = 'imconvert ' + f + ' -resize 2048x2048>50% ' + f
                print cmd
                os.system( cmd )
        except:
            traceback.print_exc()
        else:
            pass
            #print 'file:\t',f
    fd.close()
        
imageConvert('d:/seer_b/seerImages.txt')
