import datetime
import logging
import os
from netmiko import ConnectHandler

# Definir o formato de data e hora desejado
timestamp_format = '%d-%m-%Y-%Hh-%Mm-%Ss'

# Obter o timestamp atual no formato desejado
current_timestamp = datetime.datetime.now().strftime(timestamp_format)

# Nome do arquivo de log com o timestamp
log_filename = f'/var/www/html/netorch/furukawa/backup_furukawa_log/backup_{current_timestamp}.log'

# Configurar o sistema de logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'

# Configurar o arquivo de log com o formato personalizado
file_handler = logging.FileHandler(log_filename)
log_formatter = logging.Formatter(log_format, datefmt='%d-%m-%Y %H:%M:%S')  # Formato: DD-MM-YYYY HH:MM:SS
file_handler.setFormatter(log_formatter)

# Configurar o nível de log
logging.basicConfig(level=logging.INFO, handlers=[file_handler])

# Função para fazer backup de um switch Cisco via SSH usando Netmiko
def backup_switch(ip, username, password, output_file):
    try:
        # Defina os parâmetros de conexão para o dispositivo
        device = {
            'device_type': 'generic_termserver',
            #'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
            'secret': password,
            'timeout': 10,
        }

        # Crie uma conexão SSH usando Netmiko
        net_connect = ConnectHandler(**device)

        # Configurar "enable"
        net_connect.send_command('enable')

        # Configurar "terminal length 0" para evitar paginação
        output = net_connect.send_command('terminal length 0')

        # Execute o comando de backup (exemplo: 'show running-config')
        output = net_connect.send_command('show running-config')

        # Salve a saída em um arquivo
        with open(output_file, 'w') as file:
            file.write(output)

        # Feche a conexão SSH
        net_connect.disconnect()

        # Construa a mensagem de log com o nome do equipamento e o IP
        log_message = f"Backup do equipamento {name} {ip} concluído com sucesso!"
        print(log_message)
        logging.info(log_message)
        logging.info(' ' * 40)  # Separador entre as mensagens de log

    except Exception as e:
        # Construa a mensagem de erro com o nome do equipamento e o IP
        log_message = f"Erro ao fazer backup do equipamento {name} {ip}: {str(e)}"
        print(log_message)
        logging.error(log_message)
        logging.info(' ' * 40)  # Separador entre as mensagens de log

        # Se o erro for específico, execute o backup novamente
        error_message = 'Search pattern never detected in send_command_expect'
        if error_message in str(e):
            log_message_retry = f"Tentando fazer backup novamente para o equipamento {name} {ip}"
            print(log_message_retry)
            logging.info(log_message_retry)
            logging.info(' ' * 40)  # Separador entre as mensagens de log
            backup_switch(ip, username, password, output_file)

# Diretório de backup
backup_dir = '/var/www/html/netorch/furukawa/'
os.makedirs(backup_dir, exist_ok=True)

# Ler o arquivo "routers" e fazer backup de cada switch listado
with open('/usr/local/scripts/routers_furukawa-netorch', 'r') as routers_file:
    for line in routers_file:
        name, ip = line.strip().split(':')
        username = 'admin'
        password = 'admin'
        output_file = f"{backup_dir}config-backup_{name}.{current_timestamp}.cfg"
        backup_switch(ip, username, password, output_file)
