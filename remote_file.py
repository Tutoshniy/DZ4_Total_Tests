import paramiko


def upload_file(host, username, password, local_path, remote_path, port=22):
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()
