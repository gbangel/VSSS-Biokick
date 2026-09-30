# Guía de Configuración y Despliegue de Red UDP (VSSS-Biokick)

Este documento detalla el procedimiento paso a paso para la puesta en marcha de la red Wi-Fi UDP entre la PC de Control y los módulos ESP32 del equipo VSSS, utilizando el adaptador USB TP-Link en modo Hotspot.

---

## Fase 1: Alimentación y Conexión de Hardware

1. **Alimentación de la ESP32:**
   * **Pruebas de banco/escritorio:** Conectar la ESP32 a la PC mediante un cable Micro-USB o USB-C (proporciona energía y comunicación serie para depuración).
   * **Pruebas en el robot:** Utilizar un regulador de voltaje adecuado (ej. Step-Down / Buck a 5V conectado a los pines `VIN` y `GND`). **Nunca alimentar los motores desde los pines de la ESP32.**
2. **Conexión del Adaptador USB TP-Link:**
   * Conectar el adaptador Wi-Fi TP-Link USB directamente a un puerto USB de la PC (de preferencia USB 3.0 directo a la tarjeta madre, evitando hubs sin alimentación).

---

## Fase 2: Configuración de la Red Wi-Fi en Windows

1. **Activar el Hotspot de Windows:**
   * Ir a **Configuración** > **Red e Internet** > **Zona con cobertura inalámbrica móvil** (*Mobile Hotspot*).
   * Configurar los parámetros de red:
     * **Nombre de red (SSID):** `VSSS_TEAM_NET`
     * **Contraseña:** `vsss12345`
     * **Banda de red:** Seleccionar estrictamente **2.4 GHz** (la ESP32 no soporta 5 GHz).
   * Cambiar el conmutador a **Activado**.

2. **Verificar el Firewall de Windows:**
   * Ir a **Panel de Control** > **Sistema y Seguridad** > **Windows Defender Firewall** > **Permitir que una aplicación a través de Windows Defender Firewall**.
   * Buscar **Python** en la lista y asegurar que las casillas **Privada** y **Pública** estén marcadas.
   * *(Opcional)* Si existen bloqueos de paquetes UDP entrantes, desactivar temporalmente el Firewall en redes privadas para descartar interferencias.

---

## Fase 3: Carga del Código en la ESP32 (MicroPython)

1. **Subir el Script (`main.py`):**
   * Abrir Thonny o VS Code (con la extensión MicroPico).
   * Cargar el archivo con la IP correspondiente al robot (ej. `192.168.137.101` para Robot 1).
   * Guardar el archivo directamente en la memoria raíz del dispositivo con el nombre `main.py`.

2. **Verificación en Consola Serie:**
   * Presionar el botón de **Reset (EN/RST)** en la placa ESP32.
   * Verificar en la consola serie la aparición del siguiente flujo:
     ```text
     Conectando al Hotspot TP-Link (VSSS_TEAM_NET)...
     Conexión exitosa al Hotspot.
     Configuración IP: ('192.168.137.101', '255.255.255.0', '192.168.137.1', '192.168.137.1')
     Servidor UDP activo en 192.168.137.101:5005
     ```

3. **Verificación en Windows:**
   * Confirmar en el panel de *Zona con cobertura inalámbrica móvil* de Windows que figura 1 dispositivo conectado.

---

## Fase 4: Verificación Previa desde la Consola de la PC (Ping)

1. Abrir la Terminal o `CMD` en Windows.
2. Ejecutar el comando ping hacia la IP del ESP32:
   ```bash
   ping 192.168.137.101
*Criterio de éxito: Confirmar la recepción de respuestas continuas con tiempos menores a 10 ms y 0% de pérdida de paquetes ICMP.

---

## Fase 5: Ejecución del Script de Medición

1. Abrir el proyecto en VS Code.
2. Ubicarse en la raíz del repositorio o en la carpeta `communication/`.
3. Desconectar o cerrar el puerto serie en Thonny si está ocupado.
Ejecutar el script de prueba de latencia:
```
python comuncation/test_udp_metrics.py
```
4. Analizar en consola los resultados de porcentaje de pérdidas y métricas de RTT (mínimo, promedio, máximo y desviación estándar).