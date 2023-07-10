import yaml

from checkout import ssh_checkout_positive

with open("config.yaml") as f:
    data = yaml.safe_load(f)


def test_step1(deploy, make_folders, clear_folders, make_files):
    # test1
    res1 = ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                                 text="Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="ls {}".format(data['folder_out']), text="arx.7z"), "Test1 Fail"
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    # test2
    res = []
    res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                     cmd="cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                                     text="Everything is Ok"))
    res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                     cmd="cd {}; 7z e arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                                     text="Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                         cmd="ls {}".format(data['folder_ext']),
                                         text=""))
    assert all(res)


def test_step3():
    # test3
    assert ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; 7z t {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                                 text="Everything is Ok"), "Test1 Fail"


def test_step4(make_folders, clear_folders, make_files):
    # test4
    assert ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; 7z u {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                                 text="Everything is Ok"), "Test1 Fail"


def test_step5(clear_folders, make_files):
    # test5
    res = []
    res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                     cmd="cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                                     text="Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                         cmd="cd {}; 7z l arx1.7z".format(data['folder_out']), text=item))
    assert all(res)


# def test_step6():


def test_step7():
    assert ssh_checkout_positive(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="7z d {}/arx1.7z".format(data['folder_out']), text="Everything is Ok"), "Test1 Fail"
