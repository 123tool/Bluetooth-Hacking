## 📡 BT-Bluetooth Hacking

![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-red?style=for-the-badge&logo=android)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Unit](https://img.shields.io/badge/Unit-123Tool%20Intelligence-7000ff?style=for-the-badge)

Alat audit keamanan Bluetooth tingkat lanjut yang dirancang untuk pemindaian radar dan pengujian ketahanan perangkat (Stress Testing) dalam radius lokal.

---

## ⚡ Fitur Utama
- **Advanced Radar Scan:** Deteksi perangkat Bluetooth di sekitar dengan akurasi tinggi.
- **Vendor Intelligence:** Identifikasi otomatis merk perangkat (Apple, Samsung, JBL, Sony, dll).
- **Bluetooth Flood (Mode A):** Menguji stabilitas koneksi audio perangkat dengan paket banjir L2CAP.
- **Battery Drain (Mode B):** Simulasi permintaan data konstan untuk menguji manajemen daya target.
- **Remote Disconnect (Mode D):** Simulasi pemutusan koneksi (Deauth) pada perangkat aktif.

---

## 🛠️ Instalasi & Persiapan (Termux)

Pastikan perangkat Anda sudah memiliki akses **ROOT** untuk menjalankan fungsi serangan (L2CAP Flood).

1. **Update & Install Dependency:**
   ```bash
   pkg update && pkg upgrade
   pkg install python python-pip bluez termux-api
   pip install bleak

