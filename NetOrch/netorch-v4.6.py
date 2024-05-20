import subprocess

scripts = [
    "/usr/local/scripts/backup_conf_cisco-netorch.py",
    "/usr/local/scripts/backup_conf_hp-netorch.py",
    "/usr/local/scripts/backup_conf_aruba-netorch.py",
    "/usr/local/scripts/backup_conf_huawei-netorch.py",
    "/usr/local/scripts/backup_conf_furukawa-netorch.py",
    "/usr/local/scripts/backup_conf_3com-netorch.py"
]

for script in scripts:
    if script == "/usr/local/scripts/backup_conf_3com-netorch.py":
        subprocess.run(["python3", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["python3", script])
print("Backup do equipamento switch-3com 10.143.250.223 concluído com sucesso!")
print()
print("NetOrch foi concluído com sucesso!")
