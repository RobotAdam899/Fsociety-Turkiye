
import socket
import os

def aktif_ipleri_bul(modem_ip, port):
    print("[*] Ag taraniyor...")
    ipler = []
    base_ip = '.'.join(modem_ip.split('.')[:3])
    for i in range(2, 255):
        ip = f"{base_ip}.{i}"
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((ip, port))
            ipler.append(ip)
            s.close()
        except:
            continue
    return ipler

def komut_gonder(ip, port, komut):
    try:
        s = socket.socket()
        s.connect((ip, port))
        s.send(komut.encode())
        cevap = s.recv(1024).decode()
        print(f"[{ip}] => {cevap.strip()}")
        s.close()
    except Exception as e:
        print(f"[{ip}] => Baglanti hatasi: {e}")

modem_ip = input("Modem IP gir: ")
port = int(input("Port gir: "))

aktifler = aktif_ipleri_bul(modem_ip, port)
if not aktifler:
    print("[!] Aktif cihaz bulunamadi.")
    exit()

print("\n[+] Aktif cihazlar:")
for i, ip in enumerate(aktifler):
    print(f"[{i+1}] {ip}")

sec = input("\n[1] Tum cihazlara gonder\n[2] Birine gonder\n>>> ")
if sec == "1":
    hedefler = aktifler
elif sec == "2":
    index = int(input("Hangi cihaz? No: ")) - 1
    hedefler = [aktifler[index]]
else:
    print("[!] Gecersiz secim.")
    exit()

komut = input("Komut gir: ")
for hedef in hedefler:
    komut_gonder(hedef, port, komut)
