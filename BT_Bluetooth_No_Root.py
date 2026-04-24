import asyncio
from bleak import BleakScanner
import os

# Versi Ringan Tanpa Root
async def monitor():
    os.system('clear')
    print("📡 SPY-E PASSIVE MONITOR (NON-ROOT)")
    print("------------------------------------")
    
    # Hanya melakukan Scanning & Monitoring
    devices = await BleakScanner.discover()
    
    if not devices:
        print("[!] Radar bersih. Tidak ada target.")
    
    for d in devices:
        name = d.name if d.name else "Unknown"
        # Logika Intel: Deteksi jika target adalah HP/Aksesoris
        print(f"TARGET: {name} | MAC: {d.address} | RSSI: {d.rssi}dBm")
        if d.rssi > -50:
            print(">>> [!] PERINGATAN: Target berada sangat dekat!")

if __name__ == "__main__":
    while True:
        asyncio.run(monitor())
        print("\n[*] Menunggu scan berikutnya (5 detik)...")
        import time
        time.sleep(5)
