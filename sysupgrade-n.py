import paramiko
 
def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                name, value = line.split('=', 1)
                config[name.strip()] = value.strip()
            elif line:
                print(f"Warning: Skipping malformed line: {line}")
    return config
 
def create_ssh_client(server, user, password, port=22):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, username=user, password=password, port=port)
        return client
    except paramiko.SSHException as e:
        print(f"SSHException: {e}")
    except Exception as e:
        print(f"Exception: {e}")
 
def flash_image(router_ip, username, password, router_image_path):
    try:
        ssh_client = create_ssh_client(router_ip, username, password)
        if not ssh_client:
            raise Exception("Failed to establish SSH connection to the router")
        stdin, stdout, stderr = ssh_client.exec_command(f"sysupgrade -n {router_image_path}")
        print(stdout.read().decode())
        print(stderr.read().decode())
        ssh_client.close()
        print("Router firmware flashed successfully")
    except Exception as e:
        print(f"Failed to flash firmware on router: {e}")
 
if __name__ == "__main__":
    config = read_config("sysupgrade-n.txt") #.txt files consisting of the required values
    router_ip = config.get('router_ip')
    router_username = config.get('router_username')
    router_password = config.get('router_password')
    router_image_path = config.get('router_image_path')
    if not all([router_ip, router_username, router_password, router_image_path]):
        print("Error: Missing required configuration parameters.")
    else:
        flash_image(router_ip, router_username, router_password, router_image_path)