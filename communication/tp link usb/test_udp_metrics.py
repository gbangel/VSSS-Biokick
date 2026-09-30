import socket
import time
import statistics

# ---------------------------------------------------------
# CONFIGURACIÓN DE PRUEBA
# ---------------------------------------------------------
# IPs de los 3 Robots bajo la red Hotspot USB
ROBOTS_IP = {
    "Robot 1": "192.168.137.101",
    "Robot 2": "192.168.137.102",
    "Robot 3": "192.168.137.103"
}

UDP_PORT = 5005
NUM_PACKETS = 500       # Cantidad de paquetes a enviar por prueba
FREQUENCY_HZ = 50       # 50 Hz = 20 ms por ciclo (Frecuencia real VSSS)
TIMEOUT_SEC = 0.05      # 50 ms de tiempo máximo de espera por respuesta


def medir_latencia(target_ip, robot_name="ESP32"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT_SEC)

    latencies_ms = []
    lost_packets = 0
    interval = 1.0 / FREQUENCY_HZ

    print(f"\n" + "=" * 50)
    print(
        f"INICIANDO PRUEBA CON {robot_name.upper()} ({target_ip}:{UDP_PORT})")
    print(f"Enviando {NUM_PACKETS} paquetes a {FREQUENCY_HZ} Hz...")
    print("=" * 50)

    for seq in range(1, NUM_PACKETS + 1):
        start_time = time.perf_counter()

        # Formato del mensaje: SEQ_ID|TIMESTAMP
        payload = f"{seq}|{start_time}".encode('utf-8')

        try:
            # Envío de paquete
            sock.sendto(payload, (target_ip, UDP_PORT))

            # Recepción de respuesta (Echo)
            response, _ = sock.recvfrom(1024)

            end_time = time.perf_counter()
            rtt_ms = (end_time - start_time) * 1000
            latencies_ms.append(rtt_ms)

        except socket.timeout:
            lost_packets += 1

        # Control preciso del periodo de envío
        elapsed = time.perf_counter() - start_time
        time_to_sleep = interval - elapsed
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

    sock.close()

    # ---------------------------------------------------------
    # MOSTRAR RESULTADOS
    # ---------------------------------------------------------
    received = NUM_PACKETS - lost_packets
    loss_rate = (lost_packets / NUM_PACKETS) * 100

    print(f"Paquetes Enviados : {NUM_PACKETS}")
    print(f"Paquetes Recibidos : {received}")
    print(f"Paquetes Perdidos  : {lost_packets} ({loss_rate:.2f}%)")

    if latencies_ms:
        print(f"Latencia Mínima    : {min(latencies_ms):.2f} ms")
        print(f"Latencia Promedio  : {statistics.mean(latencies_ms):.2f} ms")
        print(f"Latencia Máxima    : {max(latencies_ms):.2f} ms")
        print(f"Desviación Estándar: {statistics.stdev(latencies_ms):.2f} ms")
    else:
        print("ERROR: No se recibió ninguna respuesta. Verifica la conexión Wi-Fi o el Firewall.")


if __name__ == "__main__":
    # Puedes probar un robot en específico cambiando la clave:
    medir_latencia(ROBOTS_IP["Robot 1"], "Robot 1")
