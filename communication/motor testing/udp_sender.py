import socket
import struct
import time

TARGET_IP = "192.168.1.101"
TARGET_PORT = 5005
ROBOT_ID = 1
HEADER = 0xAA


def pack_command(robot_id: int, rpm_motor: int) -> bytes:
    # Colocamos la misma consigna de RPM en ambas ruedas para mantener el paquete de 7 bytes
    raw_payload = struct.pack(
        "<BBhh", HEADER, robot_id, int(rpm_motor), int(rpm_motor))
    checksum = 0
    for b in raw_payload:
        checksum ^= b
    return raw_payload + struct.pack("<B", checksum)


def probar_un_motor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Secuencia para 1 motor: (Descripción, RPM, Duración)
    secuencia = [
        ("1. Girar hacia ADELANTE (200 RPM)", 200, 4.0),
        ("2. PARAR Motor (0 RPM)", 0, 2.0),
        ("3. Girar hacia ATRÁS (-200 RPM)", -200, 4.0),
        ("4. PARAR Motor (0 RPM)", 0, 1.0)
    ]

    print(f"=== PRUEBA DE 1 MOTOR N20 EN {TARGET_IP}:{TARGET_PORT} ===")
    interval = 1.0 / 60.0  # 60 Hz

    try:
        for desc, rpm, duracion in secuencia:
            print(f"\n{desc}")
            t_fin = time.time() + duracion

            while time.time() < t_fin:
                t_start = time.perf_counter()

                packet = pack_command(ROBOT_ID, rpm)
                sock.sendto(packet, (TARGET_IP, TARGET_PORT))

                t_elapsed = time.perf_counter() - t_start
                t_sleep = interval - t_elapsed
                if t_sleep > 0:
                    time.sleep(t_sleep)

        print("\n¡Prueba de motor finalizada!")

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    finally:
        sock.sendto(pack_command(ROBOT_ID, 0), (TARGET_IP, TARGET_PORT))
        sock.close()


if __name__ == "__main__":
    probar_un_motor()
