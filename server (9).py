
import socket
import sys

def usage():
    print("Kullanım: python server.py -p <port>")
    exit()

if len(sys.argv) != 3 or sys.argv[1] != "-p":
    usage()

try:
    port = int(sys.argv[2])
except:
    usage()

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

print(f"[*] Port: {port}")
while True:
    ip = input("Hedef IP (çıkmak için q): ").strip()
    if ip.lower() == "q":
        break
    komut = input("Komut: ").strip()
    komut_gonder(ip, port, komut)
