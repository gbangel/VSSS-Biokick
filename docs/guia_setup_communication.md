# Guía de Configuración y Despliegue de Red UDP con Router Dedicado (VSSS-Biokick)

Este documento detalla el procedimiento paso a paso para la puesta en marcha de la red Wi-Fi UDP entre la PC de Control, un Router Wi-Fi dedicado y los módulos ESP32 del equipo VSSS.

---

## Fase 1: Alimentación y Conexión de Hardware

1. **Alimentación y Conexión del Router Wi-Fi:**
   * Conectar el router a la fuente de alimentación mediante su adaptador AC/DC original.
   * Asegurarse de que el router esté encendido y que los LEDs de estado (Power, Wi-Fi 2.4 GHz) se encuentren activos de manera estable.

2. **Conexión de la PC al Router:**
   * **Vía Cable Ethernet (Recomendado):** Conectar un cable de red desde el puerto Ethernet de la PC a uno de los puertos **LAN** del router (evitar el puerto WAN/Internet).
   
3. **Alimentación de la ESP32:**
   * **Pruebas de banco/escritorio:** Conectar la ESP32 a la PC o a un cargador de 5V mediante un cable Micro-USB o USB-C (proporciona energía y comunicación serie para depuración).
   * **Pruebas en el robot:** Utilizar un regulador de voltaje adecuado (ej. Step-Down / Buck a 5V conectado a los pines `VIN` y `GND`). **Nunca alimentar los motores ni cargas inductivas desde los pines de la ESP32.**

---

## Fase 2: Configuración de la Red Wi-Fi en el Router y Windows

1. **Configuración de los parámetros del Router:**
   * Acceder al panel de administración del router desde el navegador web de la PC (usualmente `192.168.1.1` o `192.168.0.1`).
   * Configurar los siguientes parámetros en la sección inalámbrica:
     * **Nombre de red (SSID):** `ORBI15`
     * **Contraseña:** `freshraven713`
     * **Banda de red:** Activar la banda **2.4 GHz** (la ESP32 opera exclusivamente en esta frecuencia). Seleccionar opción 01.

---

## Fase 3: Carga del Código en la ESP32 (MicroPython)

1. **Subir el Script (`main.py`):**
   * Abrir Thonny IDE o VS Code (con la extensión MicroPico).
   * Modificar las credenciales de Wi-Fi (`SSID` y `Password`) en el código script e ingresar la IP fija asignada al robot (ej. `192.168.1.101` para Robot 1).
   * Guardar el archivo directamente en la memoria raíz del dispositivo con el nombre `main.py`.

2. **Verificación en Consola Serie:**
   * Presionar el botón de **Reset (EN/RST)** en la placa ESP32.
   * Verificar en la consola serie de Thonny la aparición del siguiente flujo:
     ```text
     Conectando al Router (ORBI15)...
     Conexión exitosa al Router.
     Configuración IP: ('192.168.1.101', '255.255.255.0', '192.168.1.1', '192.168.1.1')
     Servidor UDP activo en 192.168.1.101:5005
     ```

3. **Verificación en el Router:**
   * Confirmar en la lista de clientes asociados del panel web del router que la IP de la ESP32 figura como activa.

---

## Fase 4: Verificación Previa desde la Consola de la PC (Ping)

1. Abrir la Terminal o `CMD` en Windows.
2. Ejecutar el comando ping hacia la IP asignada a la ESP32:
   ```bash
   ping 192.168.1.101
   ```
   * **Criterio de éxito:** Confirmar la recepción de respuestas continuas con tiempos menores a 5 ms (idealmente < 2 ms si la PC está conectada por cable) y 0% de pérdida de paquetes ICMP.

---

## Fase 5: Ejecución del Script de Medición

1. Abrir el proyecto en VS Code.
2. Ubicarse en la raíz del repositorio o en la carpeta `communication/router/`.
3. Desconectar o cerrar el puerto serie en Thonny si está ocupado para no saturar los recursos de la placa.
4. Ejecutar el script de prueba de latencia UDP:
   ```bash
   python communication/router/test_udp_metrics.py
   ```
5. Analizar en consola los resultados de porcentaje de pérdidas de paquetes y métricas de RTT (mínimo, promedio, máximo y desviación estándar).