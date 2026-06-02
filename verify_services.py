import asyncio
from bleak import BleakClient

ADDRESS = "F2:4C:4C:14:68:D4"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected:", client.is_connected)

        for service in client.services:
            print(f"\nService: {service.uuid}")

            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
                print(f"  Properties: {char.properties}")

asyncio.run(main())
