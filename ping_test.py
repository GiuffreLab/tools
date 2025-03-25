# ping-test.sh - A CLI ping test with spinner, selectable ping count,
# flexible source IP detection (Linux, macOS, fallback for older RHEL), and RTT rounding.

# Clear the terminal
clear

# Display a header
echo "========================================="
echo "           Multi Count Ping Test"
echo "========================================="
echo ""

# Prompt the user for the remote IP address
read -p "Enter the remote IP to test: " remote_ip

# Check if an IP was provided
if [[ -z "$remote_ip" ]]; then
    echo "No IP entered. Exiting..."
    exit 1
fi

# Determine OS and capture the source IP used to reach the remote IP
os=$(uname)
if [[ "$os" == "Linux" ]]; then
    if command -v ip > /dev/null; then
        # Use ip command (common on modern Linux, including RHEL 7+)
        source_ip=$(ip route get "$remote_ip" 2>/dev/null | grep -oP 'src \K\S+')
    elif command -v ifconfig > /dev/null; then
        # Fallback using ifconfig for older RHEL systems
        source_ip=$(ifconfig | awk '/inet / && $2 != "127.0.0.1" {print $2; exit}')
    else
        source_ip="Unknown (no ip or ifconfig command found)"
    fi
elif [[ "$os" == "Darwin" ]]; then
    # macOS: determine the outgoing interface and get its IP address
    iface=$(route get "$remote_ip" 2>/dev/null | awk '/interface: / {print $2}')
    source_ip=$(ipconfig getifaddr "$iface")
else
    source_ip="Unknown (unsupported OS)"
fi

# Prompt for ping count selection
echo ""
echo "Select ping count:"
echo "1) 10"
echo "2) 100"
echo "3) 1000"
read -p "Enter your choice (1/2/3): " choice

case $choice in
    1) count=10 ;;
    2) count=100 ;;
    3) count=1000 ;;
    *) echo "Invalid choice. Defaulting to 1000 pings."
       count=1000 ;;
esac

echo ""
echo "Running $count ping test to $remote_ip..."
echo "This may take a few moments; please wait..."
echo ""

# Start the ping command in the background and redirect output to a file
ping -c "$count" -i 0.2 "$remote_ip" > ping_results.txt 2>&1 &
ping_pid=$!

# Spinner progress indicator
spinner='|/-\'
spin_index=0
while kill -0 $ping_pid 2>/dev/null; do
    spin_index=$(( (spin_index + 1) % 4 ))
    printf "\rProcessing... ${spinner:$spin_index:1}"
    sleep 0.1
done
printf "\rProcessing... Done!        \n"

# Read the ping output from the file
ping_output=$(cat ping_results.txt)

# If the ping command failed, alert the user and exit
if [ $? -ne 0 ]; then
    echo "Ping command failed. Please check the IP address and your network connectivity."
    exit 1
fi

# Parse the ping output for key statistics
transmitted=$(echo "$ping_output" | grep -oP '^\d+(?= packets transmitted)')
received=$(echo "$ping_output" | grep -oP '(?<=, )\d+(?= received)')
packet_loss=$(echo "$ping_output" | grep -oP '\d+(?=% packet loss)')

# Extract and format the RTT (round-trip time) information to 2 decimal places
rtt_line=$(echo "$ping_output" | grep "rtt")
if [ -n "$rtt_line" ]; then
    # Example RTT line: rtt min/avg/max/mdev = 58.882/149.383/429.711/114.958 ms
    rtt_values=$(echo "$rtt_line" | awk -F'=' '{print $2}' | tr -d ' ms')
    rtt_min_raw=$(echo $rtt_values | awk -F'/' '{print $1}')
    rtt_avg_raw=$(echo $rtt_values | awk -F'/' '{print $2}')
    rtt_max_raw=$(echo $rtt_values | awk -F'/' '{print $3}')
    rtt_mdev_raw=$(echo $rtt_values | awk -F'/' '{print $4}')

    rtt_min=$(printf "%.2f" "$rtt_min_raw")
    rtt_avg=$(printf "%.2f" "$rtt_avg_raw")
    rtt_max=$(printf "%.2f" "$rtt_max_raw")
    rtt_mdev=$(printf "%.2f" "$rtt_mdev_raw")
else
    rtt_min="N/A"
    rtt_avg="N/A"
    rtt_max="N/A"
    rtt_mdev="N/A"
fi

# Display the formatted results including the detected source IP
echo ""
echo "========================================="
echo "              Test Results"
echo "========================================="
printf "%-25s: %s\n" "Remote IP" "$remote_ip"
printf "%-25s: %s\n" "Source IP" "$source_ip"
printf "%-25s: %s\n" "Packets Transmitted" "$transmitted"
printf "%-25s: %s\n" "Packets Received" "$received"
printf "%-25s: %s%%\n" "Packet Loss" "$packet_loss"
printf "%-25s: %s\n" "RTT Minimum" "$rtt_min ms"
printf "%-25s: %s\n" "RTT Average" "$rtt_avg ms"
printf "%-25s: %s\n" "RTT Maximum" "$rtt_max ms"
printf "%-25s: %s\n" "RTT MDEV" "$rtt_mdev ms"
echo "========================================="
echo ""
echo "The complete ping output has been saved to 'ping_results.txt'."