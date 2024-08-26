import time
import board
import digitalio
import busio
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC
 
# LoRa Module Setup
import sys
import select
 
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
    if select.select([sys.stdin], [], [], 0.0)[0]:
        return sys.stdin.readline().strip()  # Read input from stdin if available
    return None
 
# IMU Setup
# On the Seeed XIAO Sense the LSM6DS3TR-C IMU is connected on a separate
# I2C bus and it has its own power pin that we need to enable.
imupwr = digitalio.DigitalInOut(board.IMU_PWR)
imupwr.direction = digitalio.Direction.OUTPUT
imupwr.value = True
time.sleep(0.1)
 
imu_i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
sensor = LSM6DS3TRC(imu_i2c)
 
# Configure LoRa settings
def send_lora_message(address, message):
    # Prepare the message with carriage return and line feed
    uart.write(f"AT+SEND={address},{len(message)},{message}\r\n".encode('utf-8'))
    time.sleep(0.1)  # Ensure the message is sent
 
# Set up the IMU and LoRa module
def initialize_lora():
    # Set to proprietary mode
    #uart.write(b"AT+OPMODE=1\r\n")
    #time.sleep(1)
    # Set the frequency band
    #uart.write(b"AT+BAND=923000000\r\n")
    #time.sleep(1)
    # Set the address ID
    uart.write(b"AT+ADDRESS=2\r\n")  # Set address for this device
    time.sleep(1)
 
initialize_lora()
 
# Main loop
last_sent_time = time.time()
 
while True:
    current_time = time.time()
 
    # Check if it's time to send data
    if current_time - last_sent_time >= 20:  # Send every 60 seconds
        # Read IMU data
        gyro_x, gyro_y, gyro_z = sensor.gyro
        imu_data = f"Gyro X: {gyro_x:.2f}, Y: {gyro_y:.2f}, Z: {gyro_z:.2f}"
         
        # Send data to address 1
        send_lora_message(2, imu_data)
         
        # Update the last sent time
        last_sent_time = current_time
 
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
