import logging
import vm

logging.getLogger(__name__).setLevel(logging.INFO)

def install_prerequisites(node: vm.Node):
    command = "apt update && apt install -y curl"
    # command = "whoami"
    logging.info(f"Installing prerequisites on {node.ip}.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error installing prerequisites on {node.ip}: {error}")
        return False
    else:
        logging.info(f"Prerequisites installed on {node.ip}")
        return True

def install_k3s_first_master(node: vm.Node):
    command = f"curl -sfL https://get.k3s.io | K3S_NODE_NAME={node.ip} sh -s - server --cluster-init"
    logging.info("Installing K3s on the first master node.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error installing K3s on the first master node: {error}")
        return False

    logging.info("K3s installed and cluster initialized on the first master node.")
    command = "cat /var/lib/rancher/k3s/server/node-token"
    output, error = node.execute_with_sudo(command)
    return output


def install_k3s_additional_master(node: vm.Node, primary_master_ip: str, secret_token: str):
    command = f"curl -sfL https://get.k3s.io | K3S_NODE_NAME={node.ip} K3S_TOKEN={secret_token} sh -s - server --server https://{primary_master_ip}:6443"
    logging.info("Installing K3s on the additional master node.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error installing K3s on the additional master node: {error}")
        return False
    else:
        logging.info("K3s installed and joined the cluster on the additional master node.")
        return True
    
def install_k3s_worker(node: vm.Node, primary_master_ip: str, secret_token: str):
    command = f"curl -sfL https://get.k3s.io | K3S_NODE_NAME={node.ip} K3S_URL=https://{primary_master_ip}:6443 K3S_TOKEN={secret_token} sh -"
    logging.info(f"Installing K3s on {node.ip}.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error installing K3s on {node.ip}: {error}")
        return False
    else:
        logging.info(f"K3s installed and joined the cluster on {node.ip}")
        return True

def uninstall_k3s_master(node: vm.Node):
    command = "k3s-uninstall.sh"
    logging.info(f"Uninstalling K3s on {node.ip}.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error uninstalling K3s on {node.ip}: {error}")
        return False
    else:
        logging.info(f"K3s uninstalled on {node.ip}")
        return True
    
def uninstall_k3s_worker(node: vm.Node):
    command = "k3s-agent-uninstall.sh"
    logging.info(f"Uninstalling K3s on {node.ip}.")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error uninstalling K3s on {node.ip}: {error}")
        return False
    else:
        logging.info(f"K3s uninstalled on {node.ip}")
        return True
    
def execute_kubectl(node: vm.Node, command: str):
    command = f"k3s kubectl {command}"
    logging.info(f"Executing kubectl command on {node.ip}: {command}")
    output, error = node.execute_with_sudo(command)

    if error:
        logging.error(f"Error executing kubectl command on {node.ip}: {error}")
        return False
    else:
        logging.info(f"Command executed successfully on {node.ip}")
        return output