import subprocess
import optparse
import re
from random import choice


def getUserOptions():
    parser = optparse.OptionParser()

    parser.add_option("-s", "--show", dest = "currentMacAddress", action="store_true",
                    help = "show the current mac address")

    parser.add_option("-r", "--random", dest = "randomMac", action="store_true",
                    help = "change mac address to random mac address")

    parser.add_option("-p", "--permanent", dest = "permanentMac", action="store_true",
                    help = "change mac address to original mac address")

    parser.add_option("-i", "--interface", dest = "interface",
                    help = "interface to change")
    
    parser.add_option("-m", "--mac", dest = "macAddress",
                      help = "enter the new mac address")
    
    return parser.parse_args() 


def changeMac(interface, macAddress):
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", macAddress])
    subprocess.run(["ifconfig", interface, "up"])


def control_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig.decode())

    if new_mac:
        return new_mac.group(0)
    else:
        return None
    

def generateRandomMac():
    options = "0123456789ABCDEFabcdef"
    random_mac = ""

    for i in range(6):
        temp = choice(options) + choice(options)
        random_mac += temp

        if i < 5:
            random_mac += ":"

    return random_mac


def permanentMac(interface):
    subprocess.run(["macchanger", "-p", interface])


def is_valid_mac(mac):
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(re.match(pattern, mac))

        

(user_inputs, arguments) = getUserOptions()


if not user_inputs.interface:
    print("You must enter the device (interface)")
else:
    if user_inputs.currentMacAddress:
        current_mac = control_mac(user_inputs.interface)
        print(f"Current MAC Address: {current_mac}")

    elif user_inputs.randomMac:
        old_mac = control_mac(user_inputs.interface)
        random_mac = generateRandomMac()
        changeMac(user_inputs.interface, random_mac)
        print(f"Current MAC Address: {old_mac}")
        print(f"New MAC Addres: {random_mac}")

 
    elif user_inputs.permanentMac:
        permanentMac(user_inputs.interface)

    elif user_inputs.macAddress and is_valid_mac(user_inputs.macAddress):
        current_mac = control_mac(user_inputs.interface)
        changeMac(user_inputs.interface, user_inputs.macAddress)
        new_mac = control_mac(user_inputs.interface)
        print(f"Current MAC Addres: {current_mac}")
        print(f"New MAC Addres: {new_mac}")

    else:
        print("Please enter a valid MAC address.")

