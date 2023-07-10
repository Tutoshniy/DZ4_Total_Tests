import yaml

from checkout import ssh_checkout_negative

with open("config.yaml") as f:
    data = yaml.safe_load(f)


def test_step1(clear_folders, make_files, make_bad_arx):
    # test1
    assert ssh_checkout_negative(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; 7z e badarx.7z -o{} -y".format(data['folder_badarx'], data['folder_ext']),
                                 text="ERROR"), "Test4 Fail"


def test_step2(clear_folders, make_files, make_bad_arx):
    # test2
    assert ssh_checkout_negative(host=data['host'], username=data['username'], password=data['password'],
                                 cmd="cd {}; 7z t badarx.7z".format(data['folder_badarx']),
                                 text="ERROR"), "Test5 Fail"
