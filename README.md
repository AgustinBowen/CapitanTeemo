# Capitan Teemo
## Suricata → Discord Alert Bot

Este proyecto conecta **Suricata** (IDS/IPS de red) con **Discord**.  
Cuando Suricata detecta tráfico sospechoso basado en tus reglas personalizadas, el bot envía una alerta automática a un canal de Discord.

---

## Requisitos

- Python **3.10+** (desarrollado en 3.13.7)
- **Suricata configurado como IPS con NFQUEUE en iptables**  
  Ejemplo de regla para redirigir tráfico a Suricata:
  ```bash
  sudo iptables -I INPUT -j NFQUEUE --queue-num 0
  sudo iptables -I OUTPUT -j NFQUEUE --queue-num 0
  ```
- Una cuenta de Discord con permisos para **crear un bot** y **agregarlo a un servidor**
- Acceso al archivo de logs de Suricata:  
  ```bash
  /var/log/suricata/eve.json
  ```

---

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone git@github.com:AgustinBowen/CapitanTeemo.git
   cd CapitanTeemo
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```
---

## Configuración

1. **Crear un bot en Discord**
   - Ir a [Discord Developer Portal](https://discord.com/developers/applications)
   - Crear una nueva aplicación → pestaña **Bot** → **Add Bot**
   - Copiar el **TOKEN** del bot

2. **Invitar el bot a tu servidor**
   - En la pestaña **OAuth2 → URL Generator** selecciona:
     - `bot`
     - Permisos: `Send Messages`, `Embed Links`
   - Copia la URL generada y pégala en el navegador → selecciona tu servidor → **Authorize**

3. **Obtener el ID del canal de Discord**
   - Activar **Developer Mode** en Discord (Ajustes → Avanzado)
   - Click derecho sobre el canal donde quieras las alertas → **Copiar ID**

4. **Configurar variables en `.env`**
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   DISCORD_BOT_TOKEN=tu_token_aqui
   DISCORD_CHANNEL_ID=123456789012345678
   ```

---

## Ejecución

Iniciar el bot:
```bash
python bot.py
```

Si todo está bien, deberías ver:
```
We have logged in as CapitanTimoBot#XXXX
```

Cuando Suricata detecte tráfico sospechoso (según tus reglas), aparecerá una alerta en tu canal de Discord con detalles como:
- Regla disparada
- Severidad
- IP origen y destino
- Hora exacta

---

## Personalización

- Editar la lista `REGLAS` en `bot.py` para definir qué reglas personalizadas quieres monitorear:
  ```python
  REGLAS = [4000001, 5000001, 2000001]
  ```

- Colores de severidad (en `send_alert`):
  ```python
  colores = {
      3: 0x85A492, Severidad Leve
      2: 0xF9D0B4, Severidad Media
      1: 0xD14745 Severidad Alta
  }
  ```

---

## Notas

- **Suricata debe estar corriendo en modo IPS con NFQUEUE en iptables**, de lo contrario no bloqueará tráfico ni generará alertas.  


---


Proyecto final de **Administración de Redes y Seguridad**  
by Architin777
