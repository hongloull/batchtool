import maya.cmds as cmds
#import re

   
def convertToRelativePath():
    #print zip(sourceFile,replaceFile)

    texList = cmds.ls( tex=1 )
    
    #p = re.compile(r'sourceimages\/*$')
    #p = re.compile(r'sourceimages/*$')
    #print texList
    textureFileList = []
    for tex in texList :
        #print cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 )
        if cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
            texFile = cmds.getAttr( (tex+'.fileTextureName') ).replace('/sourceimages','sourceimages')
            try:
                cmds.setAttr( (tex+'.fileTextureName'),texFile,type='string' )
                #print p.search( texFile ).group()
            except:
                print texFile
    #cmds.select( textureFileList,r=1 )    

