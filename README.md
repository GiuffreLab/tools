# Network Tools

## Overview

This repository contains two network tools: `Broom` and `Lens`. Both scripts are designed to help network administrators manage and troubleshoot their networks by providing essential network information and functionalities.

### Broom

Broom is a subnet sweeping tool that pings all IP addresses within a given subnet range to identify active hosts. It is useful for network discovery and monitoring purposes.

### Lens

Lens is a network analysis tool that calculates and displays the network address, broadcast address, and usable host range for a given IP address and either a subnet mask or CIDR notation. This tool helps network administrators understand the structure of their network and identify the range of usable IP addresses.

## Broom

### Description

Broom is designed to quickly sweep a subnet for active IP addresses by pinging each address in the range. It provides a summary of the active hosts found within the subnet.

### Usage

1. Run the script:
    ```bash
    ./broom.py
    ```

2. Follow the prompts:
    - Enter the IP address (e.g., `192.168.1.1`).
    - Enter the subnet mask or CIDR notation (e.g., `255.255.255.0` or `24`).

### Example

```bash
$ ./broom.py
-------------------------------------------------
Welcome to Broom!
Run by user_name
Broom is being run without Root privileges!
-------------------------------------------------
Please enter the IP address: 192.168.1.0
Please enter the CIDR notation: 24
-------------------------------------------------
Sweeping: 192.168.1.0/24
-------------------------------------------------
Active host found: 192.168.1.1
Active host found: 192.168.1.2
...
-------------------------------------------------
Sweep completed!
-------------------------------------------------
```

## Lens

### Description

Lens calculates and displays the network address, broadcast address, and usable host range for a given IP address and either a subnet mask or CIDR notation. This tool is helpful for network planning and management.

### Usage

1. Run the script:
    ```bash
    ./lens.py
    ```

2. Follow the prompts:
    - Enter the IP address (e.g., `192.168.1.1`).
    - Enter the subnet mask or CIDR notation (e.g., `255.255.255.0` or `24`).

### Example

```bash
$ ./lens.py
-------------------------------------------------
Welcome to Lens!
Run by user_name
Lens is being run without Root privileges!
-------------------------------------------------
Please enter the IP address: 192.168.1.1
Please enter the subnet mask or CIDR: 24
The network address is: 192.168.1.0
The broadcast address is: 192.168.1.255
Total usable hosts: 254
The usable host range is: 192.168.1.1 - 192.168.1.254
```
