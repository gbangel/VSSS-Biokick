import network
import socket
import time

# ---------------------------------------------------------
# CONFIGURACIÓN DE RED (HOTSPOT USB TP-LINK)
# ---------------------------------------------------------
WIFI_SSID = "VSSS_TEAM_NET"       # Nombre de la red de tu Hotspot
WIFI_PASS = "vsss12345"           # Contraseña configurada en Windows

# Cambiar la IP segun el robot:
# Robot 1: 192.168.137.101
# Robot 2: 192.168.137.102
# Robot 3: 192.168.137.103
ESP_IP = "192.168.137.101"
SUBNET = "255.255.255.0"
GATEWAY = "192.168.137.1"         # IP por defecto de la PC en Hotspot Windows
DNS = "192.168.137.1"

UDP_PORT = 5005


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Asignar IP estática antes de conectar para evitar DHCP
    wlan.ifconfig((ESP_IP, SUBNET, GATEWAY, DNS))

    if not wlan.isconnected():
        print(f"Conectando al Hotspot TP-Link ({WIFI_SSID})...")
        wlan.connect(WIFI_SSID, WIFI_PASS)

        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("Conexión exitosa al Hotspot.")
        print("Configuración IP:", wlan.ifconfig())
        return True
    else:
        print("Error: No se pudo conectar al Hotspot.")
        return False


def iniciar_servidor_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ESP_IP, UDP_PORT))
    sock.settimeout(0.005)  # Timeout no bloqueante corto (5 ms)
    print(f"Servidor UDP activo en {ESP_IP}:{UDP_PORT}")
    return sock


# ---------------------------------------------------------
# BUCLE PRINCIPAL
# ---------------------------------------------------------
if conectar_wifi():
    udp_socket = iniciar_servidor_udp()

    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data:
                # Responder inmediatamente el mismo paquete (Echo/Ack)
                udp_socket.sendto(data, addr)

                # Aquí tus compañeros procesarán el comando recibido
                # ej: msg = data.decode('utf-8')

        except OSError:
            # Captura el timeout normal cuando no hay datos entrantes
            pass
