import asyncio
from bleak import BleakClient

ADDRESS = "F2:4C:4C:14:68:D4"

HR_UUID = "00002a37-0000-1000-8000-00805f9b34fb"
CMD_UUID = "fd4b0002-cce1-4033-93ce-002d5875f58a"

BROADCAST_HR_ON = bytes.fromhex("aa0800a823080e016c935474")

def handle_hr(_sender, data):
    print("RAW:", data.hex())
    flags = data[0]
    hr = data[1] if flags & 0x01 == 0 else int.from_bytes(data[1:3], "little")
    print(f"Heart rate: {hr} bpm")

async def main():
    async with BleakClient(ADDRESS, timeout=20) as client:
        print("Connected:", client.is_connected)

        await client.start_notify(HR_UUID, handle_hr)
        print("HR notify started")

        try:
            print("Sending broadcast HR ON command...")
            await asyncio.wait_for(
                client.write_gatt_char(CMD_UUID, BROADCAST_HR_ON, response=False),
                timeout=5
            )
            print("Command sent")
        except Exception as e:
            print("Write failed or timed out:", repr(e))

        print("Waiting for HR...")
        while True:
            await asyncio.sleep(1)

asyncio.run(main())
