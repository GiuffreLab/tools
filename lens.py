#!/usr/bin/env python

# This Python script calculates and displays the network address,
# broadcast address, and usable host range for a given IP address
# and either a subnet mask or CIDR notation.
#
# Users will be prompted to enter an IP address and either a subnet mask or CIDR.
# The script will then compute the network and broadcast addresses, along with the range of usable hosts.
# Finally, it will print these details to the console, including the total number of usable hosts.

# How to use this script:

# from network_info import NetworkInfo

# def some_function():
#     ip = "192.168.1.1"
#     subnet = "255.255.255.0"

#     network_info = NetworkInfo()
#     network = network_info.get_network_address(ip, subnet, type)
#     broadcast = network_info.get_broadcast_address(ip, subnet, type)
#     usable = network_info.get_usable_host_range(ip, subnet, type)
#     network_info.print_results(network, broadcast, usable)

# some_function()

# The above code will print the following to the console:
# The network address is:
# The broadcast address is:
# Total usable hosts:
# The usable host range is:



# Script begins now
from colorama import Fore, Style, init
import ipaddress

class NetworkInfo:

    @staticmethod
    def get_network_address(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return network.network_address

    @staticmethod
    def get_broadcast_address(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return network.broadcast_address

    @staticmethod
    def get_usable_host_range(ip, subnet, type):
        network = ipaddress.IPv4Network(f"{ip}/{subnet}", strict=False)
        return list(network.hosts())

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


# The following block will only execute when the script is run standalone, not when imported
if __name__ == '__main__':
    init()

    ip = input(Fore.CYAN + "Please enter the IP address: " + Style.RESET_ALL)
    subnet_or_cidr = input(Fore.CYAN + "Please enter the subnet mask or CIDR: " + Style.RESET_ALL)

    if '/' in subnet_or_cidr:
        type = 'cidr'
    else:
        type = 'subnet'

    network_info = NetworkInfo()
    network = network_info.get_network_address(ip, subnet_or_cidr, type)
    broadcast = network_info.get_broadcast_address(ip, subnet_or_cidr, type)
    usable = network_info.get_usable_host_range(ip, subnet_or_cidr, type)
    network_info.print_results(network, broadcast, usable)
