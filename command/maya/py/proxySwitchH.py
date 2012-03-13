#Description:SwitchProxy for reference node (multi level reference) 
#Version:1.00
#Author:honglou(hongloull@hotmail.com)
#Create:2006.11.21
#Update:2008.05.27
#How to use : 
#      Put the script in your scripts folder
#      Source the script
#      Select some reference node first
#      Type and execute "proxySwitchH("0")"(high) or "proxySwitchH("1")"(low) in the command line or Script Editor
#
import maya.cmds as cmds
import maya.mel

def proxySwitchH(proxyTag):
    preSels = cmds.ls(selection=1)
    refSels = []
    proxyMs = []
    
    # Get seleted proxy manager 
    for preSel in preSels :
        if cmds.referenceQuery( preSel, isNodeReferenced=True ) :
            #get refernce node
            refTmp = cmds.referenceQuery( preSel,referenceNode=True )
            if refTmp in refSels:
                pass
            else :
                refSels.append( refTmp )
                #get reference proxy manager node and add to proxyMs list
                if cmds.listConnections( (refTmp+".proxyMsg"),connections=1 ) != None :
                    proxyMs.append( cmds.listConnections( (refTmp+".proxyMsg"),connections=1 )[-1] )
    print 'refSels=%s' % refSels
    print 'proxyMs=%s' % proxyMs
    
    # No proxy manager selected
    if len(proxyMs)==0:
        # Get proxy manager in this file
        proxyMs = cmds.ls(type='proxyManager')
    if len(proxyMs)==0:
        print 'There is no proxy manager in this file.'
    else:   
        for proxyM in proxyMs:
            print '\n'
            print 'proxyM=%s' % proxyM
            # Get proxy list reference
            refs = cmds.ls( cmds.listConnections( (proxyM + '.proxyList') ),type='reference')
            print 'refs=%s' %refs
            for ref in refs:
                #print cmds.getAttr( (ref +'.proxyTag') )
                if proxyTag in cmds.getAttr( (ref +'.proxyTag') ):
                    print 'proxyTag=%s' % proxyTag

                    # Get the active proxy reference
                    activeDstPlugs = cmds.connectionInfo( (proxyM + '.activeProxy'),dfs=1 )
                    if len(activeDstPlugs)==1:
                        activePlug = activeDstPlugs[0]
                        dstPlugs = cmds.connectionInfo( activePlug,dfs=1 )
                        if len(dstPlugs)==1:
                            refNode = maya.mel.eval( "plugNode " + dstPlugs[0] )
                            nodeType = cmds.nodeType( refNode )
                            if nodeType=='reference':
                                print 'refNode=%s' % refNode

                                # If proxyTag is active proxy ,then do nothing ,else switch proxy
                                if refNode!=ref:
                                    #select proxy manager and then switch proxy
                                    cmds.select(proxyM,r=1)
                                    cmd = "proxySwitch(\"" + ref + "\")"
                                    try:
                                        maya.mel.eval(cmd)
                                    except:
                                        print (proxyM + ' has no active proxy.\n')

    # Reselect obj before script executed
    if len(preSels):
        try:
            cmds.select(preSels,r=1)
        except:
            pass

## 	// Get the active proxy reference
## 	//
## 	string $activeDstPlugs[] = `connectionInfo -dfs ($proxyManager + ".activeProxy")`;
## 	if( size($activeDstPlugs) == 1 ){

## 		// Recall that the active proxy points to the entry in the proxyList
## 		// that is the active one, and not directly to the reference node
## 		// (to avoid a fan-in).
## 		//
## 		string $activePlug = $activeDstPlugs[0];
## 		string $dstPlugs[] = `connectionInfo -dfs ($activePlug)`;

## 		if( size($dstPlugs) == 1 ){

## 			string $refNode = `plugNode $dstPlugs[0]`;
## 			string $nodeType = `nodeType $refNode`;

## 			if( $nodeType == "reference" ){
