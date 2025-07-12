import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, required=True, help="Port numarası")
args = parser.parse_args()

host = "0.0.0.0"
port = args.port

s = socket.socket()
s.bind((host, port))
s.listen(1)
print(f"[+] Dinleniyor: {host}:{port}")

client, adres = s.accept()
print(f"[+] Bağlandı: {adres[0]}:{adres[1]}")

while True:
    try:
        komut = input("Komut >> ").strip()
        if not komut:
            continue
        client.send(komut.encode())
        cevap = client.recv(4096).decode()
        print(f"\n{cevap}\n")
    except KeyboardInterrupt:
        print("\n[!] Bağlantı kapatılıyor...")
        client.send("exit".encode())
        client.close()
        break
    except Exception as e:
        print(f"[X] Hata: {str(e)}")
        break
