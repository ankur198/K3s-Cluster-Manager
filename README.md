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

### Execute Commands
To execute a command on the K3s cluster, run the following command:

`python main.py execute <command>`

Example: `python main.py execute "get nodes -o wide"`

Replace <command> with the command you want to run.

### Uninstallation
To uninstall the K3s cluster, run the following command:

`python main.py uninstall`

### Screenshots

- **Install**

    ![image](https://github.com/user-attachments/assets/8946c01c-fb12-4c33-b9c0-1ed0e22c977d)

- **Execute**

    ![image](https://github.com/user-attachments/assets/a232f0a8-d567-43d7-992a-9daf4369cfbc)

- **Uninstall**

    ![image](https://github.com/user-attachments/assets/5485b262-5235-498c-af1b-085fe63b4858)


## License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
