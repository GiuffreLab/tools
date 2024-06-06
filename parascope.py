#!/bin/bash

# This script detects the network you are connected to.
# It then sweeps it to find other devices connected
# finally it will scan those devices for any open ports

# Ensure nmap, ping, and ip are available
command -v nmap >/dev/null 2>&1 || { echo "nmap not found. Exiting."; exit 1; }
command -v ping >/dev/null 2>&1 || { echo "ping not found. Exiting."; exit 1; }
command -v ip >/dev/null 2>&1 || { echo "ip not found. Use a system with the 'ip' command or modify the script to use ifconfig."; exit 1; }

# Get the current IP address and subnet
IP_ADDR=$(ip -o -f inet addr show | grep -v "127.0.0.1" | awk '{print $4}')
OCTETS=$(echo $IP_ADDR | cut -d "." -f 1,2,3)

# Create a new .txt
SCAN_FILE="${OCTETS}.txt"
echo "" > $SCAN_FILE

# Loop for multi-thread ping check last octet in network IP range
for ip in {1..254}
do
    (ping -c 1 $OCTETS.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" >> $SCAN_FILE) &
done

wait

# Perform port scan on sorted list of found IP
nmap -sS -iL $SCAN_FILE
