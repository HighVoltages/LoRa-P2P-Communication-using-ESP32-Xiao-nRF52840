import board
import busio
import time
import sys
 
# Define RX and TX pins for CircuitPython
rx_pin = board.RX  # RX pin
tx_pin = board.TX  # TX pin
 
# Initialize hardware serial
uart = busio.UART(tx=tx_pin, rx=rx_pin, baudrate=9600, timeout=2.0)  # Increased timeout to 2 seconds
 
# Initialize the serial monitor for debugging
print("Serial monitor settings:")
print("- End Char  : Newline")
print("- Baud Rate : 115200")
print()
 
# Function to handle non-blocking input
def non_blocking_input():
    import select
    # Check if data is available on stdin
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip()  # Read input from stdin if available
    return None
 
while True:
    # Check if data is available from LoRa module
    if uart.in_waiting > 0:
        data = uart.read(256)  # Read up to 256 bytes
        if data:
            print("Received:", data.decode('utf-8').strip())  # Print the data from LoRa module
 
    # Check if data is available from serial monitor
    input_data = non_blocking_input()  # Check for non-blocking input
    if input_data:
        # Append carriage return and line feed
        uart.write((input_data + '\r\n').encode('utf-8'))  # Send data to LoRa module
 
    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
