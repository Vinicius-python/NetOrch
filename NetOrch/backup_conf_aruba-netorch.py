from netmiko import ConnectHandler
import datetime
import logging

# Definir o formato de data e hora desejado
timestamp_format = '%d-%m-%Y-%Hh-%Mm-%Ss'

# Obter o timestamp atual no formato desejado
current_timestamp = datetime.datetime.now().strftime(timestamp_format)

# Nome do arquivo de log com o timestamp
#log_filename = f'/usr/local/scripts/backup_aruba_log/backup_aruba_{current_timestamp}.log'
log_filename = f'/var/www/html/riogaleao/aruba/backup_aruba_log/backup_aruba_{current_timestamp}.log'

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
            'device_type': 'hp_procurve',  # Tipo de dispositivo Cisco IOS
            'ip': ip,
            'username': username,
            'password': password,
            'secret': password,  # Senha secreta (normalmente a mesma senha)
            'timeout': 60,  # Tempo limite da conexão SSH
            #'read_timeout_override': 90,  # Tempo limite da conexão SSH
        }

        # Crie uma conexão SSH usando Netmiko
        net_connect = ConnectHandler(**device)
        
        # Testando o comando executa enter
        #output = net_connect.send_command_timing('\n')
        #net_connect.send_command("\n", expect_string=r'continue')

        # Configurar "terminal length 0" para evitar paginação
        net_connect.send_command('no page')

        # Execute o comando de backup (exemplo: 'show running-config')
        output = net_connect.send_command('show running-config')
        #read_timeout=90

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

# Ler o arquivo "routers" e fazer backup de cada switch listado
with open('/usr/local/scripts/routers_aruba-netorch', 'r') as routers_file:
    for line in routers_file:
        name, ip = line.strip().split(':')
        username = 'suporterg'
        password = 'rg#support'
        backup_switch(ip, username, password, f"/var/www/html/netorch/aruba/config-backup_{name}.{current_timestamp}.cfg")
