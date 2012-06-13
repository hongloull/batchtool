#Description:modify image f from f lists
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.07
#How to use :
import os
import sys
import traceback
import Image
import shutil

def imageResize_lms(f):
    im = Image.open(f)
    w,h = im.size
    if w>=2048 :
        try:
            f_l = f.replace('.jpg','__L.jpg')
            f_m = f.replace('.jpg','__M.jpg')
            f_s = f.replace('.jpg','__S.jpg')
            #print f1
            # rename old file
            shutil.copy(f,f_l)
                
            #cmd = 'imconvert ' + f + ' -resize 2048x2048>50% -quality 100 ' + f_l
            cmd = 'imconvert ' + f_l + ' -resize 50% -quality 100 ' + f_m
            os.system( cmd )
                
            cmd = 'imconvert ' + f_l + ' -resize 25% -quality 100 ' + f_s
            os.system( cmd )
                
        except:
            traceback.print_exc()
        else:
            pass
                
if __name__ == "__main__" :
    imageResize_lms( sys.argv[1] )
