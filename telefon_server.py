
import socket
import sys
import re

# Varsayılan değerler
IP = input("Hedef IP: ")
PORT = 7200

# Komut satırından port argümanı al
for arg in sys.argv:
    match = re.match(r"-p(\d+)", arg)
    if match:
        PORT = int(match.group(1))

print(f"[+] Bağlanıyor: {IP}:{PORT}")

while True:
    komut = input("[FSOCIETY@PHONE ~]$ ")
    if komut.strip() == "":
        continue
    try:
        s = socket.socket()
        s.connect((IP, PORT))
        s.send(komut.encode())
        cevap = s.recv(4096).decode()
        print(cevap.strip())
        s.close()
    except Exception as e:
        print(f"[!] Bağlantı hatası: {e}")
