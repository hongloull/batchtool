import sys
import os
import maya.cmds as cmds

class getPlayblastCmd(object):
    def __init__(self):
        pass
    
    def writeFile(self,file_name,cmd_file):
        f = open(file_name,'r')
        t = list()
        for l in f.readlines():
            l = l.strip()
            if l:
                t.append( self.getPlayblastCmd(l) )
            
        s= 'source headDisplay.mel;\r\npython("import digital37.maya.animation.PlayBlast_Batch as PlayBlast_Batch");\r\n' + '\n'.join(t)
        print s
        f = open(cmd_file,'w')
        f.write(s)
        f.close()
            
    def getPlayblastCmd(self,file_name):
        ext = os.path.splitext(file_name)[1]
        if ext=='.mb':
            ext = 'mayaBinary'
        else:
            ext = 'mayaAscii'
        
        cmd = 'file -f -options "v=0"  ' + ' -type \"' + ext + '\" -o \"' + file_name + '\";'
        cmd += 'python(\"PlayBlast_Batch.main()\");'
        return cmd
          
                                   
def main(files):
    getPlayblastCmd().writeFile(files[0],files[1])
    
if __name__ == '__main__' :
    main(sys.argv[1:])
    
#Z:/D031SEER/MayaProject/scenes/shot/ep30/ep30_sc0030/anim/seer_an_ep30_sc0030.mb
#Z:/D031SEER/MayaProject/scenes/shot/ep30/ep30_sc0020/anim/seer_an_ep30_sc0020.mb