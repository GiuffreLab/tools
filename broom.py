#!/usr/bin/env python

import os  # Importing os for user and privilege checks
import subprocess  # Importing subprocess to run system commands
import ipaddress  # Importing ipaddress for network calculations
from concurrent.futures import ThreadPoolExecutor  # Importing ThreadPoolExecutor for parallel execution
from colorama import Fore, Style, init  # Importing colorama for colored terminal output

# Function to check if the script is run with root privileges
def check_root():
    return os.geteuid() == 0

# Function to display the welcome message and user information
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

# Function to ping a host and check if it is active
def ping_host(ip):
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "64 bytes" in result.stdout.decode():
            print(f"Active host found: {ip}")
    except Exception as e:
        print(f"Error pinging {ip}: {e}")

# Main function to execute the sweep
def main():
    init()  # Initialize colorama

    welcome_message()  # Display welcome message

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

    # Display completion message
    print("-------------------------------------------------")
    print("\033[44mSweep completed!\033[0m")
    print("-------------------------------------------------")

# The following block will only execute when the script is run standalone, not when imported
if __name__ == "__main__":
    main()
