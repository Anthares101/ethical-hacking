# The idea of this script is to take an all port fast nmap scan output and generate the nmap command needed to enumerate the open ports more in depth.

#! /bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./nmap_command_from_ports.sh <NMAP_OUTPUT_FILE>"
    exit -1
fi

nmap_output=$(cat $1 2> /dev/null)

if [ $? -ne 0 ]; then
	echo "File not found!"
    exit -1
fi

ports_raw=$(echo $nmap_output | grep -Eo "[0-9]*/tcp|udp")
ports_parsed=$(echo $ports_raw | sed "s/\/tcp\|udp/,/g; s/\ //g; s/,$//g")

echo "nmap -sC -sV -p$ports_parsed <IP>"
