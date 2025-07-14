import socket

def ip_tara(modem_ip):
    aktifler = []
    ip_parca = ".".join(modem_ip.split(".")[:-1])
    for i in range(1, 255):
        ip = f"{ip_parca}.{i}"
        try:
            s = socket.socket()
            s.settimeout(0.2)
            s.connect((ip, PORT))
            aktifler.append(ip)
            s.close()
        except:
            pass
    return aktifler

PORT = int(input("Port gir: "))
modem_ip = input("Modem IP gir (örn: 192.168.1.1): ")

cihazlar = ip_tara(modem_ip)
if not cihazlar:
    print("[!] Aktif cihaz bulunamadi.")
    exit()

print("[*] Aktif IP'ler:")
for i, ip in enumerate(cihazlar):
    print(f"[{i+1}] {ip}")

sec = input("[>] Secilecek IP no (tumu icin *): ")
hedefler = cihazlar if sec == "*" else [cihazlar[int(sec)-1]]

for ip in hedefler:
    try:
        s = socket.socket()
        s.connect((ip, PORT))
        s.send("[✓] Baglanti kuruldu\n".encode())
        while True:
            komut = s.recv(1024).decode().strip()
            if komut == "exit":
                break
            print(f"[{ip}] Komut alindi: {komut}")
        s.close()
    except:
        print(f"[!] {ip} baglantisi basarisiz.")
