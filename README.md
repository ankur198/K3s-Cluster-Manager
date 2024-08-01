# K3s Cluster Manager

This project provides a set of scripts to manage a K3s cluster, including installation, uninstallation, and executing commands on the cluster.

## Getting Started
1. Update `nodes.yaml` file accordingly
    
    *We currently support `username`, `password` based authentication.*

1. install required dependencies `pip install -r requirements.txt`

## Available Commands

### Installation
To install the K3s cluster, run the following command:

`python main.py install`

### Uninstallation
To uninstall the K3s cluster, run the following command:

`python main.py uninstall`

### Execute Commands
To execute a command on the K3s cluster, run the following command:

`python main.py execute <command>`

Replace <command> with the command you want to run.

## License
This project is licensed under the MIT License. See the LICENSE file for details.