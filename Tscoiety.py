import requests
import threading

def send_requests(url, count):
    for i in range(count):
        try:
            response = requests.get(url)
            print(f"İstek {i+1} gönderildi, durum kodu: {response.status_code}")
        except Exception as e:
            print(f"İstek {i+1} başarısız: {e}")

def main():
    url = input("Hedef site URL'sini girin (örn: https://example.com): ").strip()
    total_requests = int(input("Gönderilecek toplam istek sayısını girin: "))
    threads_count = int(input("Kaç paralel thread çalışsın? "))

    requests_per_thread = total_requests // threads_count
    threads = []

    print(f"\n{threads_count} thread ile toplam {total_requests} istek gönderiliyor...\n")

    for _ in range(threads_count):
        t = threading.Thread(target=send_requests, args=(url, requests_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nYük testi tamamlandı.")

if __name__ == "__main__":
    main()
