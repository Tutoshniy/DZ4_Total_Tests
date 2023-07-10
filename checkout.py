import subprocess

import paramiko as paramiko


def ssh_checkout_positive(host, username, password, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname=host, username=username, password=password, port=port)
    print('Connection')
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    if exit_code == 0 and text in out:
        return True
    else:
        return False


def ssh_checkout_negative(host, username, password, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(hostname=host, username=username, password=password, port=port)
    print('Connection')
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    if exit_code != 0 and text in out:
        return True
    else:
        return False
