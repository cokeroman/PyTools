#! /opt/python/bin/python


import optparse
from socket import *
from threading import *
import re

screenLock = Semaphore(value=1)

def connScan(tgtHost, tgtPort):
    try:
        #print tgtHost + ':' + str(tgtPort)
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        if (tgtPort == 80) | (tgtPort == 8080):
            connSkt.send('HEAD / HTTP/1.1 \r\n\r\n')
            results = connSkt.recv(1024)
            reg = re.search(r'(Server:.*)\n', results)
            results = reg.group(0)
        else:
            connSkt.send('ViolentPython\r\n')
            results = connSkt.recv(1024)
        
        screenLock.acquire()
        print '\t[+]%d/tcp open' % tgtPort
        print '\t\t[+] ' + str(results)
    except:
        screenLock.acquire()
        print '\t[-]%d/tcp closed'% tgtPort
    finally:
        screenLock.release()
        connSkt.close()
        
        
def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print "[-] Cannot resolve '%s': Unknown host" % tgtHost
        return
    try:
        tgtName = gethostbyaddr(tgtIP)
        print '[+] Scan Results for: ' + tgtName[0]
    except:
        print '[+] Scan Results for: ' + tgtIP
        
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()
        t.join()
        
def main():
    parser = optparse.OptionParser('usage%prog ' + '-H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string',help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port[s] separated by comma') 
    (options, args) = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print parser.usage
        exit(0)
    portScan(tgtHost, tgtPorts)
        
        
if __name__ == "__main__":
    main()
