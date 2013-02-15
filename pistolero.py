#!/opt/python/bin/python

import optparse
import urllib2
from threading import *
#import os
from multiprocessing import *
from time import *
import random



### NO TOCAR DE AQUI PARA ABAJO SI NO SABES LO QUE HACES ###

screenLock = Semaphore(value=1)

code_200 = 0
code_404 = 0
code_500 = 0
code_506 = 0
code_otros = 0
totalrequest = 0
skipcache = False




def makeRequest(hilo, h, skipcache):
        global code_200
        global code_404
        global code_500
        global code_506
        global code_otros
        global totalrequest
        global url
        count = 0
        for r in range(request):
		try:
                        if (skipcache) and (count < 1):
                            url = url + "?r=" + str(random.randint(1,100000))
                        totalrequest += 1
			#print str(hilo) + ":" + str(totalrequest)
                        req = urllib2.Request(url, headers=h)
			response = urllib2.urlopen(req)
                        if response.getcode() == 200:
                            code_200 += 1
                except urllib2.HTTPError, e:
                        if e.code == 404:
                            code_404 += 1
                        elif e.code == 500:
                            code_500 += 1
                        elif e.code == 506:
                            code_506 += 1
                        else:
                            code_otros += 1
                count += 1
        print "\t[+] Request Procesadas" +  ': ' + str(totalrequest)
        
def main():
    
        global url
#        global uri
#        global user_agent
#        global referer
        global request
        global code_200
        global code_404
        global code_500
        global code_506
        global code_otros
        parser = optparse.OptionParser('./pistolero.py ' + '-H <Host Headert> -d <ip address> -u <request uri> -c <threads> -r <request per thread> [--stress] [--skipcache]')
        parser.add_option('-H', dest='host', type='string',help='Especifica la cabecera de host')
        parser.add_option('-d', dest='ip', type='string', help='Direccion IP o nombre de host del servidor') 
        parser.add_option('-u', dest='uri', type='string', help='Especifica la Request URI') 
        parser.add_option('-c', dest='concurrent', type='int', help='Especifica el numero de threads') 
        parser.add_option('-r', dest='request', type='int', help='Especifica el numero de Request por Thread') 
        parser.add_option('--stress', dest='stress', action="store_true", help='Optional, si esta presente se cambia el modo de benchmark a stress, lanzando las request en paralelo. Carece de estadisticas') 
        parser.add_option('--skipcache', dest='skipcache', action="store_true", help='Optional, Para evitar una cache o proxy intermedio') 



        (options, args) = parser.parse_args()

        host = options.host
        ip = options.ip
        uri = options.uri
        concurrent = options.concurrent
        request = options.request
        stress = options.stress
        skipcache = options.skipcache
        
        if (host == None) | (ip == None) | (uri == None) | (concurrent == None) | (request == None):
            print parser.usage
            exit(0)
 
        url = 'http://' + ip + uri
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'
        referer = 'http://www.servotic.com'

        h = { 'Host' : host,
            'User-Agent' : user_agent,
            'Referer' : referer
	}    
    
    
        ts_ini = time()
        print " [*] URL: " + url + "\t(Host: " + host + ")"
        
        # Lanzamos el proceso X veces
	for i in range(concurrent):
                if not stress:
                    p = Thread(target=makeRequest, args=(i, h, skipcache,))
                    p.start()
                    p.join()
                else:
                    p = Process(target=makeRequest, args=(i, h, skipcache,))
                    p.start()
                
        ts_fin = time()
        # Calculamos el tiempo de ejecucion
        exec_time = ts_fin - ts_ini
        
        #Calculamos las request por segundo
        reqxs = totalrequest / exec_time
        
        if not stress:
            print "\n\t[+] Resumen:"
            print "\t\t[-] Tiempo de ejecucion: %.2f segundos" % exec_time
            print "\t\t[-] Request por segundo: %.2f req/s" % reqxs
            print "\t\t[-] Code 200:\t\t" + str(code_200)
            print "\t\t[-] Code 404:\t\t" + str(code_404)
            print "\t\t[-] Code 500:\t\t" + str(code_500)
            print "\t\t[-] Code 506:\t\t" + str(code_506)
            print "\t\t[-] Code Other:\t\t" + str(code_otros)
            print 

if __name__ == '__main__':
	main()

