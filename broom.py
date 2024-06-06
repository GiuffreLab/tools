#!/usr/bin/env python

import os
import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

def check_root():
    return os.geteuid() == 0

def welcome_message():
    user_name = os.getlogin()
    print("-------------------------------------------------")
    print("Welcome to Broom!")
    print(f"Run by \033[35m{user_name}\033[0m")
    if check_root():
        print("Broom is being run \033[31mwith\033[0m Root privileges!")
    else:
        print("Broom is being run \033[32mwithout\033[0m Root privileges!")
    print("-------------------------------------------------")

def ping_host(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "64 bytes" in result.stdout.decode():
            print(f"Active host found: {ip}")
    except Exception as e:
        print(f"Error pinging {ip}: {e}")

def main():
    init()
    welcome_message()

    # Ask for the IP address and CIDR separately
    ip = input(Fore.CYAN + "Please enter the IP address: " + Style.RESET_ALL)
    cidr = input(Fore.CYAN + "Please enter the CIDR notation: " + Style.RESET_ALL)
    cidr_subnet = f"{ip}/{cidr}"

    # Calculate the IP range
    network = ipaddress.ip_network(cidr_subnet, strict=False)
    ip_list = list(network.hosts())

    # Display the chosen subnet before starting the sweep
    print("-------------------------------------------------")
    print(f"Sweeping: \033[36m{cidr_subnet}\033[0m")
    print("-------------------------------------------------")

    # Start the sweep
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(ping_host, ip_list)

    print("-------------------------------------------------")
    print("\033[44mSweep completed!\033[0m")
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()
