import asyncio
from bleak import BleakScanner, BleakClient
import platform
DEVICE_NAME = "NanoBLE_Math"
CHAR_UUID = "abcdefab-1234-1234-1234-abcdefabcdef"

# OS SYSTEM

os_name = platform.system()
if os_name == "Linux":
    DEVICE_CLIENT = "4A:B5:E2:CE:28:F9" # adresse arduino
elif os_name == "Darwin": # Mac
    DEVICE_CLIENT = "103C2028-FCA3-6BF9-F00A-BE9AC00C3DDA"
else:
    print("Windows non supporté")
    exit()


class BluetoothHandler:
    def __init__(self):
        self.data = None
        self.running = True
        self.client = None
        self.ready = asyncio.Event()

    def notification_handler(self, sender, data):
        try:
            message = data.decode("utf-8")
            self.data = message
        except:
            self.data = str(data)

    async def connect(self):
        print("[*] Scan BLE en cours...")
        devices = await BleakScanner.discover()

        target = None
        for d in devices:
            print(d)
            if d.address == DEVICE_CLIENT:
                target = d

        if target is None:
            print("[*] Arduino non trouvée.")
            return

        print("[*] Connecté à", target.name)

        self.client = BleakClient(target.address)
        await self.client.connect()
        while not self.client.services:
            await asyncio.sleep(0.1)
        await self.client.start_notify(CHAR_UUID, self.notification_handler)
        self.ready.set()

        """async with BleakClient(target.address) as client:
            await client.start_notify(CHAR_UUID, self.notification_handler)

            while self.running:
                await asyncio.sleep(0.05)"""

    def run(self):
        asyncio.create_task(self.connect())

    def get_data(self):
        return self.data
    
    async def send_command(self, cmd):
        await self.ready.wait()
        if self.client and self.client.is_connected:
            await self.client.write_gatt_char("beb5483e-36e1-4688-b7f5-ea07361b26a8", cmd.encode())