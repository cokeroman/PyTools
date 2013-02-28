#!/bin/bash


#IP="82.223.246.162"
IP="82.223.133.18"
#IP="82.223.245.228"
VHOST="www.servotic.com"
URI="/wp-content/themes/servotic/style.css"
REQ=10


time_connect=0
first_byte=0
dns_time=0
time_total=0
time_pretransfer=0

echo " [+] $VHOST ($IP)"
for i in `seq 1 $REQ`
do
	DATA=`curl -o /dev/null -w "%{http_code} %{time_connect} %{time_starttransfer} %{time_namelookup} %{time_total} %{time_pretransfer}\n" -H "Host: ${VHOST}" ${IP}/${URI} 2> /dev/null`
	TC=`echo $DATA | awk '{print $2}' | sed -e "s/,//"`
	FB=`echo $DATA | awk '{print $3}' | sed -e "s/,//"`
	DNST=`echo $DATA | awk '{print $4}' | sed -e "s/,//"`
	TT=`echo $DATA | awk '{print $5}' | sed -e "s/,//"`
	TP=`echo $DATA | awk '{print $6}' | sed -e "s/,//"`

#	echo $DATA 

	time_connect=`expr $time_connect + $TC`
	first_byte=`expr $first_byte + $FB`
	dns_time=`expr $dns_time + $DNST`
	time_total=`expr $time_total + $TT`
	time_pretransfer=`expr $time_pretransfer + $TP`

	echo " 	  [+] Test $i of $REQ"
	echo "		[-] Time Connect: $TC ms"
	echo "		[-] First Byte: $FB ms"
	echo "		[-] DNS Time: $DNST ms"
	echo "		[-] Download Time: $TP ms"
	echo "		[-] Total time: $TT ms"
done

# Calculamos la media
time_connect=`expr $time_connect / $REQ`
first_byte=`expr $first_byte / $REQ`
dns_time=`expr $dns_time / $REQ`
time_total=`expr $time_total / $REQ`
time_pretransfer=`expr $time_pretransfer / $REQ`

echo " [+] Summary for $VHOST ($IP) (Time Average): "
echo "		[-] Time Connect: $time_connect ms"
echo "		[-] First Byte: $first_byte ms"
echo "		[-] DNS Time: $dns_time ms"
echo "		[-] Download Time: $time_pretransfer ms"
echo "		[-] Total time: $time_total ms"

