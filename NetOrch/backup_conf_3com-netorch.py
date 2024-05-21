import datetime
import logging
from netmiko import ConnectHandler

# Definir o formato de data e hora desejado
timestamp_format = '%d-%m-%Y-%Hh-%Mm-%Ss'

# Obter o timestamp atual no formato desejado
current_timestamp = datetime.datetime.now().strftime(timestamp_format)

# Nome do arquivo de log com o timestamp
log_filename = f'/var/www/html/riogaleao/3com/backup_3com_log/backup_{current_timestamp}-unit1.log'

# Configurar o sistema de logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# Configurar o arquivo de log com o formato personalizado
file_handler = logging.FileHandler(log_filename)
log_formatter = logging.Formatter(log_format, datefmt='%d-%m-%Y %H:%M:%S')  # Formato: DD-MM-YYYY HH:MM:SS
file_handler.setFormatter(log_formatter)

# Configurar o nível de log
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

# Função para fazer backup de um switch 3Com via SSH usando Netmiko
def backup_switch(ip, username, password):
    hostname = ''
    try:
        # Criar uma conexão SSH usando Netmiko
        device = {
            'device_type': 'hp_comware_ssh',
            'ip': ip,
            'username': username,
            'password': password,
        }
        ssh_client = ConnectHandler(**device)

        # Executar o comando TFTP para fazer backup do arquivo de configuração
        hostname = ssh_client.find_prompt().strip('#')
        command = f'tftp 10.143.4.41 put unit1>flash:/3comoscfg.cfg /3com/netorch/{name}.{current_timestamp}.cfg'
        output = ssh_client.send_command_timing(command)
        print(output)

        # Fechar a conexão SSH
        ssh_client.disconnect()

        # Construir a mensagem de log com o nome do equipamento e o IP
        log_message = f"Backup do equipamento {name} {ip} concluído com sucesso!"
        print(log_message)
        logging.info(log_message)
        logging.info(' ' * 40)  # Separador entre as mensagens de log

    except Exception as e:
        # Construir a mensagem de erro com o nome do equipamento e o IP
        log_message = f"Erro ao fazer backup do equipamento {name} {ip}: {str(e)}"
        print(log_message)
        logging.error(log_message)
        logging.info(' ' * 40)  # Separador entre as mensagens de log

# Ler o arquivo "routers_3com" e fazer backup de cada switch listado
with open('/usr/local/scripts/routers_3com-netorch', 'r') as routers_file:
    for line in routers_file:
        name, ip = line.strip().split(':')
        username = 'admin'
        password = 'admin'
        backup_switch(ip, username, password)
