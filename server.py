import socket
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Dinlenecek port numarası", required=True)
    args = parser.parse_args()
    PORT = args.port

    try:
        s = socket.socket()
        s.bind(("0.0.0.0", PORT))
        s.listen(1)
        print(f"[✓] Dinleniyor: 0.0.0.0:{PORT}")
    except Exception as e:
        print(f"[!] Port hatası: {e}")
        return

    try:
        client, addr = s.accept()
        print(f"[✓] Bağlandı: {addr}")
        print(client.recv(1024).decode())
    except Exception as e:
        print(f"[!] Bağlantı hatası: {e}")
        return

    while True:
        try:
            komut = input("Komut > ").strip()
            if not komut:
                continue
            client.send(komut.encode())
            if komut == "exit":
                break
            yanit = client.recv(4096).decode()
            print(yanit)
        except Exception as e:
            print(f"[!] Bağlantı koptu: {e}")
            break

if __name__ == "__main__":
    main()
