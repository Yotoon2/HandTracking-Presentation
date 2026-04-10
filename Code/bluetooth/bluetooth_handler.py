import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "NanoBLE_Math"
CHAR_UUID = "abcdefab-1234-1234-1234-abcdefabcdef"

def notification_handler(sender, data):
    try:
        message = data.decode("utf-8")
        print("Reçu :", message)
    except:
        print("Reçu brut :", data)

async def main():
    print("Scan BLE en cours...")
    devices = await BleakScanner.discover()

    target = None
    for d in devices:
        print(f"Trouvé : {d.name} | {d.address}")
        if d.name == DEVICE_NAME:
            target = d

    if target is None:
        print("Arduino non trouvée.")
        return

    print(f"\nConnexion à {target.name} ({target.address})...")

    async with BleakClient(target.address) as client:
        print("Connecté")

        await client.start_notify(CHAR_UUID, notification_handler)

        print("En écoute...\n")

        while True:
            await asyncio.sleep(1)

asyncio.run(main())