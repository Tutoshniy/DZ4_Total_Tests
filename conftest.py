import random
import string

import paramiko
import pytest
import yaml
import time

from remote_file import upload_file
from checkout import ssh_checkout_positive

with open("config.yaml") as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="mkdir {} {} {} {}".format(data['folder_in'],
                                                                   data['folder_out'], data['folder_ext'],
                                                                   data['folder_badarx']), text="")


@pytest.fixture()
def clear_folders():
    return ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
        cmd="rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                            data['folder_badarx']), text="")


@pytest.fixture()
def make_files():
    list_off_files = []
    for i in range(5):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=data['count_files']))
        if ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                cmd="cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data['folder_in'], filename,
                                                                                       data['size_file']),
                text=""):
            list_off_files.append(filename)
    return list_off_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; mkdir {}".format(data['folder_in'], subfoldername), text=""):
        return None, None
    if not ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
            cmd="cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'], subfoldername,
                                                                                      testfilename), text=""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                          cmd="cd {}; 7z a {}/arxbad".format(data['folder_in'], data['folder_out']),
                          text='Everything is Ok')
    ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                          cmd='truncate -s 1 {}/arxbad.7z'.format(data['folder_out']), text='Everything is Ok')
    yield 'arxbad'
    ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                          cmd='rm -f {}/arxbad.7z'.format(data['folder_out']), text='')


@pytest.fixture(autouse=True)
def write_stat():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with open(data['stat_file'], 'r') as f:
        cpu_stats = f.read()

    stat_info = '{}, {}, {}, {}\n'.format(current_time, data['count_files'], data['size_file'], cpu_stats)

    with open(data['output_file'], 'a') as f:
        f.write(stat_info)


@pytest.fixture(scope='session')
def deploy():
    res = []
    upload_file(host=data['host'], username=data['username'], password=data['password'], local_path=data['local_path'],
                remote_path=data['remote_path'])
    res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                     cmd='echo "2222" | sudo -S dpkg -i {}'.format(data['remote_path']),
                                     text='Настраивается пакет'))
    res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                     cmd='echo "2222" | sudo -S dpkg -s p7zip-full',
                                     text='Status: install ok installed'))
    assert res
