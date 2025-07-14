import socket
import argparse

# Komut satırından port alma
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, required=True, help="Dinlenecek port")
args = parser.parse_args()
PORT = args.port

# Sunucu başlatılıyor
s = socket.socket()
try:
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    print(f"[✓] Dinleniyor: 0.0.0.0:{PORT}")
except Exception as e:
    print(f"[!] Port hatasi: {e}")
    exit()

# Bağlantı bekleniyor
try:
    client, addr = s.accept()
    print(f"[✓] Baglandi: {addr}")
    print(client.recv(1024).decode())
except Exception as e:
    print(f"[!] Baglanti hatasi: {e}")
    exit()

# Komut döngüsü
while True:
    try:
        komut = input("Komut > ").strip()
        if not komut:
            continue
        client.send(komut.encode())
        if komut == "exit":
            break
        cevap = client.recv(4096).decode()
        print(cevap)
    except Exception as e:
        print(f"[-] Baglanti koptu: {e}")
        break
