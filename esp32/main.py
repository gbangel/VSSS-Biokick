import network
import socket
import time

# ---------------------------------------------------------
# CREDENCIALES Y RED NETGEAR ORBI RBR50v2
# ---------------------------------------------------------
WIFI_SSID = "ORBI15"
WIFI_PASS = "freshraven713"

ESP_IP = "192.168.1.101"
SUBNET = "255.255.255.0"
GATEWAY = "192.168.1.1"
DNS = "192.168.1.1"

UDP_PORT = 5005


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)

    try:
        wlan.disconnect()
    except Exception:
        pass

    wlan.active(False)
    time.sleep(1)

    wlan.active(True)
    time.sleep(0.5)

    # ---------------------------------------------------------
    # ¡PASO CRÍTICO!: DESACTIVAR MODO DE AHORRO DE ENERGÍA
    # ---------------------------------------------------------
    try:
        wlan.config(pm=wlan.PM_NONE)
        print("Modo de ahorro de energía Wi-Fi DESACTIVADO (PM_NONE).")
    except Exception as e:
        print("Advertencia: No se pudo configurar PM_NONE:", e)

    print(f"Conectando a la red Wi-Fi: '{WIFI_SSID}'...")
    wlan.connect(WIFI_SSID, WIFI_PASS)

    timeout = 15
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        wlan.ifconfig((ESP_IP, SUBNET, GATEWAY, DNS))
        print("\n¡Conexión exitosa!")
        print("Configuración de red asignada:", wlan.ifconfig())
        return True
    else:
        print("\nError: No se pudo conectar al Wi-Fi.")
        return False


def iniciar_servidor_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ESP_IP, UDP_PORT))
    sock.settimeout(0.005)
    print(f"Servidor UDP escuchando en {ESP_IP}:{UDP_PORT}")
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
                # Responder inmediatamente para medición de latencia RTT
                udp_socket.sendto(data, addr)
        except OSError:
            pass
