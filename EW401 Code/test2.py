from bleak import BleakScanner
import asyncio
import math

PUCK_ADDRESS = "D854E3C7-0A99-82E0-32AE-957542745F8F"  # Replace with your Puck.js address


def calculate_distance(rssi, tx_power=-59):
    """
    Estimate distance based on RSSI and Tx Power.
    :param rssi: Received Signal Strength Indicator (dB)
    :param tx_power: Measured RSSI at 1 meter (dB)
    :return: Estimated distance in meters
    """
    if rssi == 0:
        return -1.0  # Unable to determine distance

    ratio = rssi / tx_power
    if ratio < 1.0:
        return math.pow(ratio, 10)
    else:
        return (0.89976) * math.pow(ratio, 7.7095) + 0.111


async def monitor_rssi():
    """
    Scans for the Puck.js and prints the RSSI and estimated distance every 0.5 seconds.
    """
    print(f"Scanning for Puck.js with address {PUCK_ADDRESS}...")
    try:
        while True:
            devices = await BleakScanner.discover()
            found = False
            for device in devices:
                if device.address == PUCK_ADDRESS:
                    found = True
                    rssi = device.rssi
                    distance = calculate_distance(rssi)
                    print(f"RSSI: {rssi} dBm, Estimated Distance: {distance:.2f} meters")
            if not found:
                print(f"Puck.js ({PUCK_ADDRESS}) not found. Ensure it is advertising.")
            await asyncio.sleep(0.5)  # Update every 0.5 seconds
    except KeyboardInterrupt:
        print("RSSI monitoring stopped.")


async def main():
    await monitor_rssi()


if __name__ == "__main__":
    asyncio.run(main())
