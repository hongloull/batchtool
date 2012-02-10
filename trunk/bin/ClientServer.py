#!/usr/bin/env python
#Description:Batch tool for maya and operation system
#Version:1.00
#Author:honglou(hongloull@hotmail.com)
#Create:2008.01.27
#Update:2009.03.09
import socket
from twisted.internet import stdio, reactor, protocol
from twisted.protocols import basic
import re

class DataForwardingProtocol(protocol.Protocol):
    def __init__(self):
        self.output = None
        self.normalizeNewlines = False
    def dataReceived(self, data):
        if self.normalizeNewlines:
            data = re.sub(r"(\r\n|\n)", "\r\n", data)
            if data == '***GOODBYE***' :
                reactor.stop()
        if self.output:
            self.output.write(data)

class StdioProxyProtocol(DataForwardingProtocol):
     def connectionMade(self):
        inputForwarder = DataForwardingProtocol( )
        inputForwarder.output = self.transport
        inputForwarder.normalizeNewlines = True
        stdioWrapper = stdio.StandardIO(inputForwarder)
        self.output = stdioWrapper
        #print "Connected to server.  Press ctrl-C to close connection."

class StdioProxyFactory(protocol.ClientFactory):
    protocol = StdioProxyProtocol
    def clientConnectionLost(self, transport, reason):
        reactor.stop( )
    def clientConnectionFailed(self, transport, reason):
        print reason.getErrorMessage( )
        reactor.stop( )

def Run(host,port,data):
    reactor.connectTCP( host, port, StdioProxyFactory() )
    reactor.run( )

if __name__ == '__main__':
    import sys
    if not len(sys.argv) == 4:
        print "Usage: %s host port" % __file__
        sys.exit(1)
    else:
        Run( sys.argv[1],int(sys.argv[2]) )
