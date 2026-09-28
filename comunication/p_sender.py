import socket

IP_ESP32 = "127.0.0.1"
PUERTO = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("PC - Control del robot VSSS")
print("Escribe un comando para enviarlo.")
print("Escribe 'salir' para terminar.\n")

while True:

    comando = input("Comando: ")

    if comando.lower() == "salir":
        break

    sock.sendto(
        comando.encode("utf-8"),
        (IP_ESP32, PUERTO)
    )

    print("Comando enviado.\n")

sock.close()
