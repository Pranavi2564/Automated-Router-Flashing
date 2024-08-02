import paramiko
from scp import SCPClient
 
def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                name, value = line.split('=', 1)  # Split on the first '='
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
 
def upload_image_to_router(router_ip, router_username, router_password, local_image_path, router_image_path):
    try:
        ssh_client = create_ssh_client(router_ip, router_username, router_password)
        if not ssh_client:
            raise Exception("Failed to establish SSH connection to the router")
        scp_client = SCPClient(ssh_client.get_transport())
        scp_client.put(local_image_path, router_image_path)
        scp_client.close()
        print("Image uploaded to router successfully")
    except Exception as e:
        print(f"Failed to upload image to router: {e}")
 
if __name__ == "__main__":
    config = read_config('local_router.txt') #.txt file consisting of the required values
    router_ip = config.get('router_ip')
    router_username = config.get('router_username')
    router_password = config.get('router_password')
    local_image_path = config.get('local_image_path')
    router_image_path = config.get('router_image_path')
    ssh_client=upload_image_to_router(router_ip, router_username, router_password, local_image_path, router_image_path)