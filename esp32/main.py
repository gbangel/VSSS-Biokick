import socket
import time
import network
import select

# ---------------------------------------------------------
# CONFIGURACIÓN DE RED Y SOCKET
# ---------------------------------------------------------
WIFI_SSID = "VSSS_TEAM_NET"
WIFI_PASS = "tu_contrasena_wifi"

ESP_IP = "192.168.1.101"
SUBNET = "255.255.255.0"
GATEWAY = "192.168.1.1"
DNS = "192.168.1.1"

UDP_PORT = 5005


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Configurar IP estática para evitar latencia de DHCP
    wlan.ifconfig((ESP_IP, SUBNET, GATEWAY, DNS))

    if not wlan.isconnected():
        print(f"Conectando a la red {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("Conexión Wi-Fi establecida con éxito.")
        print("Configuración de red:", wlan.ifconfig())
        return True
    else:
        print("Error al conectar a la red Wi-Fi.")
        return False


def iniciar_servidor_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ESP_IP, UDP_PORT))
    # Timeout no bloqueante para el socket
    sock.settimeout(0.01)
    print(f"Escuchando paquetes UDP en {ESP_IP}:{UDP_PORT}")
    return sock


# ---------------------------------------------------------
# BUCLE PRINCIPAL (MAIN LOOP)
# ---------------------------------------------------------
if conectar_wifi():
    udp_socket = iniciar_servidor_udp()

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data:
                # Echo inmediato del mismo paquete recibido
                udp_socket.sendto(data, addr)

                # Aquí irá el desglose de datos para el PID / Motores
                # ej: mensaje = data.decode('utf-8')

        except OSError:
            # Timeout del socket cuando no hay datos entrantes (esperado)
            pass
