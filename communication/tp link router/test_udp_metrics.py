import socket
import time
import statistics

# ---------------------------------------------------------
# CONFIGURACIÓN
# ---------------------------------------------------------
TARGET_IP = "192.168.1.101"  # IP del ESP32 físico
TARGET_PORT = 5005
NUM_PACKETS = 1000           # Cantidad de paquetes para el test
FREQUENCY_HZ = 50            # 50 Hz = 1 paquete cada 20ms (Estándar VSSS)
TIMEOUT_SEC = 0.05           # 50 ms de timeout por paquete

# ---------------------------------------------------------
# EJECUCIÓN DE PRUEBA DE RED
# ---------------------------------------------------------


def run_latency_test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT_SEC)

    latencies_ms = []
    lost_packets = 0
    interval = 1.0 / FREQUENCY_HZ

    print(f"Iniciando prueba UDP hacia {TARGET_IP}:{TARGET_PORT}")
    print(f"Enviando {NUM_PACKETS} paquetes a {FREQUENCY_HZ} Hz...")
    print("-" * 50)

    for seq in range(1, NUM_PACKETS + 1):
        start_time = time.perf_counter()

        # Estructura del payload: SEQ_ID|TIMESTAMP
        payload = f"{seq}|{start_time}".encode('utf-8')

        try:
            sock.sendto(payload, (TARGET_IP, TARGET_PORT))
            response, _ = sock.recvfrom(1024)

            end_time = time.perf_counter()
            rtt_ms = (end_time - start_time) * 1000
            latencies_ms.append(rtt_ms)

        except socket.timeout:
            lost_packets += 1

        # Control preciso de frecuencia de envío
        elapsed = time.perf_counter() - start_time
        time_to_sleep = interval - elapsed
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    sock.close()

    # ---------------------------------------------------------
    # RESUMEN Y MÉTRICAS
    # ---------------------------------------------------------
    received_packets = NUM_PACKETS - lost_packets
    loss_rate = (lost_packets / NUM_PACKETS) * 100

    print("\n" + "=" * 50)
    print("RESULTADOS DEL TEST DE LATENCIA Y PÉRDIDA DE PAQUETES")
    print("=" * 50)
    print(f"Paquetes Enviados : {NUM_PACKETS}")
    print(f"Paquetes Recibidos : {received_packets}")
    print(f"Paquetes Perdidos  : {lost_packets} ({loss_rate:.2f}%)")

    if latencies_ms:
        print(f"Latencia Mínima    : {min(latencies_ms):.2f} ms")
        print(f"Latencia Promedio  : {statistics.mean(latencies_ms):.2f} ms")
        print(f"Latencia Máxima    : {max(latencies_ms):.2f} ms")
        print(f"Desviación Estándar: {statistics.stdev(latencies_ms):.2f} ms")
    else:
        print("ERROR: No se recibió ningún paquete. Revisa la IP o el Firewall.")


if __name__ == "__main__":
    run_latency_test()
