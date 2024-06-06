#!/usr/bin/bash

clear

USER_NAME=$(id -un)
    echo -------------------------------------------------
    echo "Welcome to Broom!"
    echo -e "Run by \e[35m${USER_NAME}\e[0m"
# Display if the user is the root user or not

if [[ "${UID}" -eq 0 ]]
then
    echo -e "Broom is being run \e[31mwith\e[0m Root privledges!"
else
    echo -e "Broom is being run \e[32mwithout\e[0m Root privledges!"
fi
    echo -------------------------------------------------

# Ask what subnet to sweep for active hosts
echo "Enter the subnet to sweep for active hosts: "
echo -e "\e[32mExample: 192.168.1.\e[0m"
read -p "Subnet: " SUBNET

# Display the chosen subnet before starting the sweep
    echo -------------------------------------------------
    echo -e "Sweeping: \e[36m$SUBNET\e[0m"
    echo -------------------------------------------------

wait

# Start the sweep
for ip in {1..254}
do
    ping -c 1 $SUBNET$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
done

sleep 1

# Display completed sweep
    echo -------------------------------------------------
    echo -e "\e[44mSweep completed!\e[0m"
    echo -------------------------------------------------
