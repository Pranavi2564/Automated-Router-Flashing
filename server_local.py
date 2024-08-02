import paramiko
from scp import SCPClient
 
def read_config(config_file):
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                name, value = line.split('=', 1)
                config[name] = value
            else:
                #print(f"Skipping invalid config line: {line}")
                break
    return config
 
def create_ssh_client(server, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=user, password=password)
    return client
 
def download_image_via_scp(remote_ip, remote_image_path, local_image_path, username, password):
    try:
        ssh_client = create_ssh_client(remote_ip, username, password)
        scp_client = SCPClient(ssh_client.get_transport())
        scp_client.get(remote_image_path, local_image_path)
        scp_client.close()
        print("Image downloaded successfully")
    except Exception as e:
        print(f"Failed to download image: {e}")
 
if __name__ == "__main__":
    config = read_config('server_local.txt') #file consisting of the required values
    remote_ip = config.get('remote_ip')
    remote_image_path = config.get('remote_image_path')
    local_image_path = config.get('local_image_path')
    username = config.get('username')
    password = config.get('password')
    if all([remote_ip, remote_image_path, local_image_path, username, password]):
        download_image_via_scp(remote_ip, remote_image_path, local_image_path, username, password)
    else:
        print("Configuration is missing required values")