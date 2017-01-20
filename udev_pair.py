#!/usr/bin/env python

import subprocess
import os, sys

def get_usb_serial_id():

    # bash command to get serial of usb drive
    get_usb_serial = "udevadm info -a -n /dev/ttyUSB0 | grep '{serial}' | head -n1"

    # run bash command and pipe output
    p = subprocess.Popen(get_usb_serial, stdout=subprocess.PIPE, shell=True)
    print("Getting USB Serial Adapter device ID...")

    # read output
    usb_serial_output = p.stdout.read()

    # strip output
    serial = str(usb_serial_output).strip()

    return serial


def udev_pair(serial_value):
    # udev rule file to create if doesn't exist
    udev_rule_path = '/etc/udev/rules.d/10-local.rules'

    # get current working directory
    cwd = os.getcwd()

    # temp udev rule file
    tmp = '10-local.rules'

    # udev rule to add
    rules = [
        '# pair usb serial adapter: ' + serial_value + ', give it a persistent name (created by clicker)\n',
        'KERNEL=="ttyUSB*", SUBSYSTEM=="tty", ' + serial_value + ', SYMLINK+="usb_serial"\n'
    ]


    # create temporary file from scratch
    with open(tmp, 'a+') as temp:
        # iterate over rules list
        for rule in rules:
            # write one line at a time
            temp.write(rule)
        # close file when done writing
        temp.close()

    print("Creating temporary udev rule file...")

    temp_file = open(tmp, 'rt').read()

    print("Checking if /etc/udev/rules.d/10-local.rules exists...")

    # check if udev rule file already exists
    if not os.path.exists(udev_rule_path):
        print("File DOES NOT exist")
        # if file DOES NOT exist do this

        # move tmp file to /etc/udev/rules.d
        os.system("sudo mv " + tmp + " " + udev_rule_path)
        print("Moving temp file...")

        # reset udev rules
        os.system("sudo udevadm control --reload-rules")
        print("Reloading udev rules...")

    # otherwise, check if file DOES exist
    elif os.path.exists(udev_rule_path):
        print("File DOES exist...")
        # if file DOES exist do this:
        # open and read existing file
        with open(udev_rule_path, 'rt') as existing_file:
            # concat existing file and new tmp file
            new_file = existing_file.read() + '\n' + temp_file
            with open(tmp, 'wt') as output:
                output.write(new_file)

        print("Adding udev rule...")
        # move tmp file to /etc/udev/rules.d
        os.system("sudo mv " + tmp + " " + udev_rule_path)
        print("Moving temp file...")

        # reset udev rules
        os.system("sudo udevadm control --reload-rules")
        print("Reloading udev rules...")



if __name__ == "__main__":
    udev_pair(get_usb_serial_id())

