from bleak import BleakScanner
# bleak is a Python module that allows you to interact with Bluetooth Low Energy (BLE) devices.
import asyncio
# asyncio is a library to write concurrent code using the async/await syntax.
import math
import threading
# threading is a module that allows you to run multiple threads in a single process.

TARGET_NAME = "JuanPuck"  # The specific name of your Puck.js
TARGET_MAC = "D854E3C7-0A99-82E0-32AE-957542745F8F"  # The specific MAC address of your Puck.js
1
running = False  # Flag to control the scanning loop to start or stop the process of scanning for the puck.js using 1 or 0 respectively.



# Step 1: BLE Scanner to find Puck.js

async def find_puckjs():
    # Scans for Puck.js with the specific name continuously while running is True.
    global running
    while running:
        print(f"Scanning for BLE devices with name: {TARGET_NAME}")
        devices = await BleakScanner.discover()
        # await is used to pause the execution of the program until the BleakScanner discovers the devices.

        found = False
        # Flag to check if the Puck.js is found or not
        for device in devices:
            # Loop through the discovered devices
            if device.name == TARGET_NAME:
                found = True
                rssi = device.rssi
                # device.rssi returns the Received Signal Strength Indicator (RSSI) of the device which is in dBm (decibels per milliwatt)
                distance = calculate_distance(rssi)
                # Calculate the distance in meters based on the RSSI using the function below
                print(f"Found {TARGET_NAME} - Address: {device.address}, RSSI: {rssi}, Estimated Distance: {distance:.2f} meters")
        
        if not found:
            print(f"No devices found with the name: {TARGET_NAME}")
        await asyncio.sleep(0.5)
        # asyncio.sleep is used to pause the execution of the program for 0.5 seconds before the next iteration of scanning.

# Step 2: Calculate Distance from RSSI

def calculate_distance(rssi, tx_power=-65.25):
    # Estimate distance based on RSSI and Tx Power.
    # rssi: Received Signal Strength Indicator (dB), used for distance estimation
    # tx_power: Measured signal strength (RSSI) at 1 meter, reference point for calculating distances based on RSSI
    # return: Estimated distance in meters
    if rssi == 0:
        return -1.0  # Unable to determine distance

    ratio = rssi / tx_power
    # Calculate the ratio of the received signal strength to the reference signal strength at 1 meter
    if ratio < 1.0:
        return math.pow(ratio, 10)
    # If the ratio is less than 1, use the power function to estimate the distance
    else:
        return (0.89976) * math.pow(ratio, 7.7095) + 0.111
    # 0.89976 and 7.7095 and 0.111 are constants used in the distance estimation formula. These values depend on environment and hardware, so for now we are using the default values until we recalibrate the system.

# Step 3: Start Scanning

def start_scanning():
    # Starts the scanning loop in an asyncio event loop.
    asyncio.run(find_puckjs())
    # asyncio.run is used to run the find_puckjs function in an asyncio event loop.

# Step 4: Main Function

def main():
    print("Enter '1' to start scanning, '0' to stop.")
    # Print the instructions for the user
    while True:
        # Infinite loop to wait for user input
        user_input = input()
        # Read the user input
        if user_input == "1":
            global running
            running = True
            # If '1', start the scanning loop
            t = threading.Thread(target=start_scanning)
            # Create a new thread to run the start_scanning function
            t.start()
            # Start the thread
        elif user_input == "0":
            running = False
            # If '0', stop the scanning loop
            break
            # Exit the loop and stop the program

if __name__ == "__main__":
    main()
    # Run the main function when the script is executed

