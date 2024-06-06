#!/usr/bin/env python

# This Python script calculates and displays the network address,
# broadcast address, and usable host range for a given IP address
# and either a subnet mask or CIDR notation.

from colorama import Fore, Style, init  # Importing colorama for colored terminal output
import os  # Importing os for user and privilege checks
import ipaddress  # Importing ipaddress for network calculations

class NetworkInfo:
    # Static method to get the network address
    @staticmethod
    def get_network_address(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return network.network_address

    # Static method to get the broadcast address
    @staticmethod
    def get_broadcast_address(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return network.broadcast_address

    # Static method to get the range of usable hosts
    @staticmethod
    def get_usable_host_range(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return list(network.hosts())

    # Static method to print the results
    @staticmethod
    def print_results(network, broadcast, usable):
        print(Fore.GREEN + "The network address is: " + Style.RESET_ALL + str(network))
        print(Fore.GREEN + "The broadcast address is: " + Style.RESET_ALL + str(broadcast))

        total_usable_hosts = len(usable)
        print(Fore.GREEN + "Total usable hosts: " + Style.RESET_ALL + str(total_usable_hosts))

        if total_usable_hosts == 0:
            print("No usable host in this subnet.")
        else:
            print(Fore.GREEN + "The usable host range is: " + Style.RESET_ALL + f"{usable[0]} - {usable[-1]}")

# Function to check if the script is run with root privileges
def check_root():
    return os.geteuid() == 0

# Function to display the welcome message and user information
def welcome_message():
    user_name = os.getlogin()
    print("-------------------------------------------------")
    print("Welcome to Lens!")
    print(f"Run by \033[35m{user_name}\033[0m")
    if check_root():
        print("Lens is being run \033[31mwith\033[0m Root privileges!")
    else:
        print("Lens is being run \033[32mwithout\033[0m Root privileges!")
    print("-------------------------------------------------")

# The following block will only execute when the script is run standalone, not when imported
if __name__ == '__main__':
    init()  # Initialize colorama

    welcome_message()  # Display welcome message

    # Prompt user for IP address and subnet mask or CIDR
    ip = input(Fore.CYAN + "Please enter the IP address: " + Style.RESET_ALL)
    subnet_or_cidr = input(Fore.CYAN + "Please enter the subnet mask or CIDR: " + Style.RESET_ALL)

    # Determine if the input is a subnet mask or CIDR
    if '/' in subnet_or_cidr:
        type = 'cidr'
    else:
        type = 'subnet'

    # Create NetworkInfo object and calculate network details
    network_info = NetworkInfo()
    network = network_info.get_network_address(ip, subnet_or_cidr, type)
    broadcast = network_info.get_broadcast_address(ip, subnet_or_cidr, type)
    usable = network_info.get_usable_host_range(ip, subnet_or_cidr, type)
    
    # Print the results
    network_info.print_results(network, broadcast, usable)
