import socket

IP = "127.0.0.1"
PUERTO = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PUERTO))

print(f"ESP32 simulada escuchando en {IP}:{PUERTO}")
print("Esperando comandos...\n")

while True:
    datos, direccion = sock.recvfrom(1024)

    comando = datos.decode("utf-8")

    print(f"Comando recibido: {comando}")
    print(f"Enviado desde: {direccion}\n")
