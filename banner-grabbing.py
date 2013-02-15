#!/usr/bin/env python

import socket



def retBanner(ip, port):
	try:
		socket.setdefaulttimeout(2)
		s= socket.socket()
		s.connect((ip, port))
		banner = s.recv(1024)
		if banner:
			print ip + ':' + str(port) + '=> open' 
		return banner
	except Exception, e:
#                print '[-] Error: ' + str(e)
		return

def checkVulns(banner):
	if 'FreeFloat Ftp Server (Version 1.00)' in banner:
		print '[+] FreeFloat FTP Server is vulnerable.'
	elif '3Com 3CDaemon FTP Server Version 2.0' in banner:
		print '[+] 3CDaemon FTP Server is vulnerable.'
	elif 'Ability Server 2.34' in banner:
		print '[+] Ability FTP Server is vulnerable.' 
	elif 'Sami FTP Server 2.0.2' in banner:
		print '[+] Sami FTP Server is vulnerable.' 
	else:
		print '[-] FTP Server is not vulnerable.'
	return



def main():

	portList = [21,22,25,80,110,443]
	hostList = ['gtools1', 'gtools2']
	
	for host in hostList:
		for port in portList:
			banner = retBanner(host, port)
			if banner:
                		print '	[+]' + host + ':' + str(port) + '=>'  + banner
				#checkVulns(banner)

if __name__ == '__main__':
	main()
