import paramiko  # pip install paramiko
import logging
import time

logging.getLogger(__name__).setLevel(logging.INFO)

paramiko_logger = logging.getLogger("paramiko")
paramiko_logger.setLevel(logging.WARNING)


class Node:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def _create_ssh_client(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username=self.username, password=self.password)
        return ssh

    def execute(self, command):
        logging.info(f"Executing command on {self.ip}: {command}")
        ssh = self._create_ssh_client()
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        if error:
            logging.error(f'Error executing command on {self.ip}: {error}')
        logging.debug(output)
        return output, error
    
    def execute_with_sudo(self, command):
        logging.info(f"Executing command on {self.ip}: sudo ({command})")
        ssh = self._create_ssh_client()
        shell = ssh.invoke_shell()
        shell.send("sudo -s\n")
        time.sleep(1)
        shell.send(f"{self.password}\n")
        time.sleep(1)
        shell.send(f"echo 'sudoBegin' && {command} && echo 'sudoDone' ; echo 'sudoError'\n")

        output = ""
        is_error = False
        while not shell.recv_ready():
            time.sleep(0.1)
        while True:
            if shell.recv_ready():
                newOutput = shell.recv(1024).decode()
                # print(newOutput)
                output += newOutput

            if output.count("sudoDone") == 2:
                break
            elif output.count("sudoError") == 2:
                is_error = True
                break

            time.sleep(0.1)

        ssh.close()
        logging.debug(output)
        if is_error:
            error = output.split("sudoBegin")[-1].split("sudoError")[0].strip()
            logging.error(f'Error executing command on {self.ip}: {error}')
            return None, error
        else:
            output = output.split("sudoBegin")[-1].split("sudoDone")[0].strip()
            return output, None

