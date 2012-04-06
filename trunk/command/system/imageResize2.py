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
import Image
import shutil

def imageResize2(fileName):
    fd = open(fileName,'r').readlines()
    fl = open('d:/seer_b/seerImages_large.txt','w')
    for f in fd:
        f = f.splitlines()[0].replace('\\','/')
        print f
        im = Image.open(f)
        w,h = im.size
        if w>2048 :
            # write file to log
            fl.write(f+'\n')
#            try:
#                f_l = f.replace('.jpg','_L.jpg')
#                f_m = f.replace('.jpg','_M.jpg')
#                f_s = f.replace('.jpg','_S.jpg')
#                #print f1
#                # rename old file
#                shutil.copy(f,f_l)
#                
#                #cmd = 'imconvert ' + f + ' -resize 2048x2048>50% -quality 100 ' + f_l
#                cmd = 'imconvert ' + f_l + ' -resize 50% -quality 100 ' + f_m
#                os.system( cmd )
#                
#                cmd = 'imconvert ' + f_l + ' -resize 25% -quality 100 ' + f_s
#                os.system( cmd )
#                
#            except:
#                traceback.print_exc()
#            else:
#                pass
                
                #print 'file:\t',f
    fl.close()
        
imageResize2('d:/seer_b/seerImages.txt')
