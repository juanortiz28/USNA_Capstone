from bleak import BleakScanner
import math
import asyncio
import threading

TARGET_NAME = "JuanPuck"  # The specific name of your Puck.js
running = False  # Flag to control the scanning loop


def calculate_distance(rssi, tx_power=-63):
    # TX_POWER is the 
    """
    Estimate distance based on RSSI and Tx Power.
    :param rssi: Received Signal Strength Indicator (dB)
    :param tx_power: Measured RSSI at 1 meter (dB)
    :return: Estimated distance in meters
    """
    if rssi == 0:
        #rssi stands for received signal strength indicator, it is a measure of the power level that a RF (Bluetooth devices or wifi) device receives from another device (Puck.js)
        return -1.0  # Unable to determine distance

    ratio = rssi / tx_power
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return (0.89976) * math.pow(ratio, 7.7095) + 0.111


async def scan_for_puckjs():
    """
    Scans for Puck.js with the specific name continuously while running is True.
    """
    global running
    while running:
        print(f"Scanning for BLE devices with name: {TARGET_NAME}...")
        devices = await BleakScanner.discover()

        found = False
        for device in devices:
            if device.name == TARGET_NAME:
                found = True
                rssi = device.rssi
                distance = calculate_distance(rssi)
                print(f"Found {TARGET_NAME} - Address: {device.address}, RSSI: {rssi}, Estimated Distance: {distance:.2f} meters")
        
        if not found:
            print(f"No devices found with the name: {TARGET_NAME}")
        await asyncio.sleep(0.5)  


def start_scanning():
    """
    Starts the scanning loop in an asyncio event loop.
    """
    asyncio.run(scan_for_puckjs())


def main():
    global running
    print("Enter '1' to start scanning, '0' to stop.")

    while True:
        user_input = input("Your choice: ").strip()
        if user_input == '1' and not running:
            print("Starting scan...")
            running = True
            scan_thread = threading.Thread(target=start_scanning)
            scan_thread.start()
        elif user_input == '0' and running:
            print("Stopping scan...")
            running = False
            break
        else:
            print("Invalid input. Enter '1' to start or '0' to stop.")


if __name__ == "__main__":
    main()
