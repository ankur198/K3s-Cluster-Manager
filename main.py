import logging
import vm, commands
import argparse
import yaml

logging.basicConfig(level=logging.INFO)

yaml_file = open("nodes.yaml")
nodes = yaml.load(yaml_file, Loader=yaml.FullLoader)

master_nodes = [
    vm.Node(node["ip"], node["username"], node["password"]) for node in nodes["master"]
]
worker_nodes = [
    vm.Node(node["ip"], node["username"], node["password"]) for node in nodes["worker"]
]


def install():
    for node in master_nodes + worker_nodes:
        commands.install_prerequisites(node)

    first_master = master_nodes[0]
    secret_token = commands.install_k3s_first_master(first_master)

    for master_node in master_nodes[1:]:
        commands.install_k3s_additional_master(
            master_node, first_master.ip, secret_token
        )

    for worker_node in worker_nodes:
        commands.install_k3s_worker(worker_node, first_master.ip, secret_token)


def uninstall():
    for worker_node in worker_nodes:
        commands.uninstall_k3s_worker(worker_node)

    for master_node in master_nodes:
        commands.uninstall_k3s_master(master_node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("K3s Cluster Manager")
    parser.add_argument("action", choices=["install", "uninstall", "execute"])
    parser.add_argument(
        "command", nargs="?", help="Command to run when action is 'execute'"
    )
    args = parser.parse_args()

    if args.action == "install":
        install()
    elif args.action == "uninstall":
        uninstall()
    elif args.action == "execute":
        if args.command:
            print(commands.execute_kubectl(master_nodes[0], args.command))
        else:
            print("Error: 'execute' action requires a command to run.")
