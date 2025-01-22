from bleak import BleakScanner
import asyncio
import math
from collections import deque

PUCK_ADDRESS = "D854E3C7-0A99-82E0-32AE-957542745F8F"  # Replace with your Puck.js address


def calculate_weighted_distance(rssi, tx_power=-59, environment_factor=2.0):
    if rssi == 0:
        return -1.0
    return 10 ** ((tx_power - rssi) / (10 * environment_factor))


class RSSISmoother:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def add(self, rssi):
        self.values.append(rssi)
        return sum(self.values) / len(self.values)


async def monitor_rssi():
    print(f"Scanning for Puck.js with address {PUCK_ADDRESS}...")
    smoother = RSSISmoother(window_size=10)
    try:
        while True:
            devices = await BleakScanner.discover()
            for device in devices:
                if device.address == PUCK_ADDRESS:
                    smoothed_rssi = smoother.add(device.rssi)
                    distance = calculate_weighted_distance(smoothed_rssi, tx_power=-62, environment_factor=2.5)
                    print(f"Smoothed RSSI: {smoothed_rssi:.2f} dBm, Estimated Distance: {distance:.2f} meters")
            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped monitoring RSSI.")


if __name__ == "__main__":
    asyncio.run(monitor_rssi())
