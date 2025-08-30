import discord
import dotenv
import json
import asyncio
from dateutil import parser
import pyfiglet
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)  

def print_animado(text):
    ascii_banner = pyfiglet.figlet_format(text)
    colors = [Fore.LIGHTBLUE_EX]
    for i, line in enumerate(ascii_banner.split("\n")):
        color = colors[i % len(colors)]
        for char in line:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(0.002)  
        print()  
        
def print_alerta(regla_nombre, regla_id, src_ip, dest_ip, hora, severity):
    severity_colors = {
        3: Fore.GREEN,
        2: Fore.YELLOW,
        1: Fore.RED
    }
    color = severity_colors.get(severity, Fore.MAGENTA)
    
    print(f"{Style.BRIGHT}{'-'*50}")
    print(f"{color}Nueva Alerta {Style.RESET_ALL}")
    print(f"{Fore.WHITE}Regla: {Style.BRIGHT}{regla_nombre} (ID: {regla_id})")
    print(f"{Fore.WHITE}Origen: {Style.BRIGHT}{src_ip}")
    print(f"{Fore.WHITE}Destino: {Style.BRIGHT}{dest_ip}")
    print(f"{Fore.WHITE}Hora: {Style.BRIGHT}{hora}")
    print(f"{color}Severidad: {severity}")
    print(f"{Style.BRIGHT}{'-'*50}\n")


DISCORD_BOT_TOKEN = dotenv.get_key(dotenv.find_dotenv(), 'DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(dotenv.get_key(dotenv.find_dotenv(), 'DISCORD_CHANNEL_ID'))

REGLAS = [4000001, 5000001, 2000001,6000001,7000001,8000001,1000002]  

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print_animado("CapitanTimo")
    print(f'Estas loguedo como {client.user}')
    client.loop.create_task(follow_log('/var/log/suricata/eve.json', send_alert))
        
async def follow_log(file_path, callback):
    with open(file_path, 'r') as f:
        f.seek(0, 2)  
        while True:
            line = f.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            try:
                data = json.loads(line)
                await callback(data)
            except json.JSONDecodeError:
                continue
                
async def send_alert(data):
    if data.get('event_type') == 'alert':
        regla_id = data.get('alert', {}).get('signature_id')
        if regla_id in REGLAS:
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            src_ip = data.get('src_ip')
            dest_ip = data.get('dest_ip')
            regla_nombre = data.get('alert', {}).get('signature')
            severity = data.get('alert', {}).get('severity', 1)
            ts = parser.isoparse(data.get("timestamp"))
            hora_detallada = ts.strftime("%Y-%m-%d %H:%M:%S")
            colores= {3: 0x85A492, 2: 0xF9D0B4, 1: 0xD14745}
            color = colores.get(severity,0xD49873)
            embed = discord.Embed(
                title="Capitan Teemo A Servicio! - Alerta de Seguridad",
                description="Se ha detectado tráfico sospechoso.",
                color=color,
                timestamp=ts  
            )
            embed.add_field(name="Regla", value=f"{regla_nombre} (ID: {regla_id})", inline=False)
            embed.add_field(name="Origen", value=src_ip, inline=True)
            embed.add_field(name="Destino", value=dest_ip, inline=True)
            embed.add_field(name="Hora", value=hora_detallada, inline=False)
            embed.set_footer(text=f"Severidad: {severity}")

            print_alerta(regla_nombre, regla_id, src_ip, dest_ip, hora_detallada, severity)

            await channel.send(embed=embed)

client.run(DISCORD_BOT_TOKEN)
