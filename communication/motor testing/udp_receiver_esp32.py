import network
import socket
import struct
import time
from machine import Pin, PWM

# ---------------------------------------------------------
# CONFIGURACIÓN DE RED Y PROTOCOLO
# ---------------------------------------------------------
ROBOT_ID = 1
WIFI_SSID = "ORBI15"
WIFI_PASS = "freshraven713"
ESP_IP = f"192.168.1.10{ROBOT_ID}"
UDP_PORT = 5005
FAILSAFE_TIMEOUT_MS = 200
HEADER = 0xAA

led = Pin(2, Pin.OUT)

# ---------------------------------------------------------
# HARDWARE UN SOLO MOTOR N20 (30:1) Y L298N
# ---------------------------------------------------------
# Canal A del L298N
ENA = PWM(Pin(25), freq=1000)
IN1 = Pin(26, Pin.OUT)
IN2 = Pin(27, Pin.OUT)

# Encoder del Motor N20 (Canal A)
ENC_A = Pin(34, Pin.IN)

# Parámetros físicos N20 30:1
PULSOS_POR_VUELTA = 7 * 30  # 210 PPR
RPM_MAXIMAS = 300

ticks = 0


def encoder_isr(pin):
    global ticks
    ticks += 1


ENC_A.irq(trigger=Pin.IRQ_RISING, handler=encoder_isr)

# ---------------------------------------------------------
# FUNCIONES
# ---------------------------------------------------------


def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    try:
        wlan.disconnect()
    except Exception:
        pass
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)

    try:
        wlan.config(pm=wlan.PM_NONE)  # Desactivar modo de ahorro de energía
    except Exception:
        pass

    wlan.connect(WIFI_SSID, WIFI_PASS)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        wlan.ifconfig((ESP_IP, '255.255.255.0', '192.168.1.1', '192.168.1.1'))
        print(f"--- PRUEBA UN MOTOR LISTA ---")
        print(f"IP: {ESP_IP}:{UDP_PORT}")
        return True
    return False


def aplicar_velocidad_motor(rpm_objetivo):
    # Sentido de giro
    if rpm_objetivo >= 0:
        IN1.value(1)
        IN2.value(0)
    else:
        IN1.value(0)
        IN2.value(1)

    # Conversión directa a PWM
    duty = int((min(abs(rpm_objetivo), RPM_MAXIMAS) / RPM_MAXIMAS) * 65535)
    ENA.duty_u16(duty)


def detener_motor():
    IN1.value(0)
    IN2.value(0)
    ENA.duty_u16(0)
    led.value(0)


# ---------------------------------------------------------
# BUCLE PRINCIPAL
# ---------------------------------------------------------
if conectar_wifi():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ESP_IP, UDP_PORT))
    sock.settimeout(0.005)

    last_packet_time = time.ticks_ms()
    last_print_time = time.ticks_ms()

    print("Esperando paquetes de la PC...")

    while True:
        try:
            data, _ = sock.recvfrom(1024)
            if len(data) == 7:
                hdr, r_id, rpm_izq, rpm_der, chk_rec = struct.unpack(
                    "<BBhhB", data)

                if hdr == HEADER and r_id == ROBOT_ID:
                    chk_calc = 0
                    for b in data[:6]:
                        chk_calc ^= b

                    if chk_calc == chk_rec:
                        # Usa únicamente rpm_izq
                        aplicar_velocidad_motor(rpm_izq)
                        last_packet_time = time.ticks_ms()
                        led.value(1)

                        # Muestra la velocidad real medida por el encoder cada 500 ms
                        if time.ticks_diff(time.ticks_ms(), last_print_time) > 500:
                            rpm_medida = (ticks / PULSOS_POR_VUELTA) * 120
                            ticks = 0
                            print(
                                f"[UDP OK] SetPoint: {rpm_izq} RPM | Medido: {rpm_medida:.1f} RPM")
                            last_print_time = time.ticks_ms()

        except OSError:
            pass

        # Failsafe (200 ms)
        if time.ticks_diff(time.ticks_ms(), last_packet_time) > FAILSAFE_TIMEOUT_MS:
            detener_motor()
