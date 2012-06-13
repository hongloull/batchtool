#Description:modify image f from f lists
#Author:honglou(hongloull@hotmail.com)
#Create:2008.03.07
#Update:2008.03.07
#How to use :
import os
import sys
import traceback

def imageResize_tga2jpg(f):
    if os.path.isfile(f) :
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
    else:
        print '%s is not exists.' % fileName
#
#def get_file(fList):
#    fileLists = list()
#    if fList:
#        for f in fList:
#            if os.path.isfile(f) :
#                fileLists.append(f)
#            elif os.path.isdir(f) :
                
        
    

if __name__ == "__main__" :
    imageResize_tga2jpg( sys.argv[1] )