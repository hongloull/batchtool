import maya.cmds as cmds

def replFileTextureName(sourceFile,replaceFile):
    #print zip(sourceFile,replaceFile)
    if sourceFile:
        if replaceFile:
            texList = cmds.ls( tex=1 )
            print texList
            textureFileList = []
            for tex in texList :
                print 1
                #print cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 )
                if cmds.attributeQuery( 'fileTextureName',node=tex,exists=1 ):
                    print 2
                    texFile = cmds.getAttr( (tex+'.fileTextureName') )
                    #for sourceF,replaceF in zip(sourceFile,replaceFile) :
                    print 'texFile=',texFile
                    if texFile.startswith( sourceFile ) :
                        print 3
                        #cmds.select( tex,r=1 )
                        print 'texFile.replace( sourceF,replaceF )=',texFile.replace( sourceFile,replaceFile )
                        cmds.setAttr( (tex+'.fileTextureName'),texFile.replace( sourceFile,replaceFile ),type='string' )
            #cmds.select( textureFileList,r=1 )     

    
