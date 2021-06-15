import os
import wget
from lastversion import lastversion 
import nmap


def check_magisk_update():
    version = 0.0

    print("[+]Checking if Magisk is downloaded...")
    for file in os.listdir():
        if file.endswith(".apk"):
            version = file[7:12]
            current = file
            print("Magisk "+ version + "is downloaded\n")
            break;
    
    latest_version = lastversion.has_update(repo = "topjohnwu/Magisk", current_version = str(version))

    print("[+]Checking if " + version + "is the latest release...")
    if (latest_version != False):
        print("Latest release is not installed\n")
        print("[+]Dowloading latest release...")
        wget.download(("https://github.com/topjohnwu/Magisk/releases/download/v"+str(latest_version)+"/Magisk-v"+str(latest_version)+".apk"), "Magisk-v"+str(latest_version)+".apk")
        print("Latest release downloaded\n")
        print("[+]Removing old release...")
        os.remove(current)
        print("Old release removed\n")


def check_vbox_installed():
    sudo = "echo test | sudo -S "
    output = os.popen(sudo + "apt list virtualbox").readlines()

    print("[+]Checking if VirtualBox is installed...")
    try:
        temp = output[1]

    except:
        print("VirtualBox is not installed\n")
        print("[+]Installing VirtualBox...")
        os.system(sudo + "apt install virtualbox")
        print("VirtualBox is installed\n")

    else:
        print("VirtualBox is installed\n")

def check_adb_installed():
    sudo = "echo test | sudo -S "
    output = os.popen(sudo + "apt list adb").readlines()

    print("[+]Checking if ADB is installed...")
    try:
        temp = output[1]

    except:
        print("ADB is not installed\n")
        print("[+]Installing ADB...")
        os.system(sudo + "apt install adb")
        print("ADB is installed\n")

    else:
        print("ADB is installed\n")

def check_vm_installed():
    output = os.popen("vboxmanage list vms").readlines()
    install_check_flag = True

    print("[+]Checking if Virtual Machine is installed...")
    for i in range(len(output)):
        if output[i][1:7] == "Magisk":
            print("Virtual Machine is installed\n")
            install_check_flag = False
            break;

    if install_check_flag:
        print("Virtual Machine is not installed\n")
        print("[+]Creating Virtual Machine...")
        os.system("vboxmanage createvm --name Magisk --register")
        print("Virtual machine has been created\n")
        print("[+]Setting up Virtual Machine...")
        os.system("vboxmanage modifyvm Magisk --ostype Linux_64 --memory 3280MB --cpus 1 --cpuexecutioncap 100 --pae on --graphicscontroller vboxvga --nic1 hostonly --cableconnected1 on --autostart-enabled on")
        print("Virtual Machine has been set up\n")
        print("[+]Creating Storage Controller...")
        os.system("vboxmanage storagectl Magisk --name 'IDE Controller' --add ide")
        print("Storage Controller has been created\n")
        print("[+]Attaching Disk Image to Virtual Machine...")
        os.system("Disk Image has been attached\n")

def start_vm():
    error_check_flag = True
    print("[+]Starting Virtual Machine...")
    os.system("vboxmanage startvm Magisk")

    output = os.popen("vboxmanage list runningvms").readlines()
    for i in range(len(output)):
        if output[i][1:7] == "Magisk":
            print("Virtual Machine has been started\n")
            check_flag = False
            break;

    if error_check_flag:
        print("Virtual Machine could not start\n")


def stop_vm():
    print("[+]Stopping Virtual Machine...")
    os.system("vboxmanage controlvm Magisk poweroff")
    print("Virtual Machine has been stopped\n")


def check_nmap_installed():
    sudo = "echo test | sudo -S "
    output = os.popen(sudo + "apt list nmap").readlines()

    print("[+]Checking if nmap is installed...")
    try:
        temp = output[1]

    except:
        print("nmap is not installed\n")
        print("[+]Installing nmap...")
        os.system(sudo + "apt install nmap")
        print("nmap is installed\n")

    else:
        print("nmap is installed\n")

def find_vm_ip():
    print("[+]Finding Virtual Machine's Network Name...")
    mac = os.popen("vboxmanage showvminfo Magisk | grep MAC").readline()[34:46]
    temp = ""
    count = 0
    for char in mac:
        if count%2 != 0 and count != 11:
            temp = temp+char+"-"
        else:
            temp = temp+char
        count += 1
    mac = temp
    netname = "android-dhcp-9-"+mac+".lan"
    print("Virtual Machine's Network Name Found ("+netname+")\n")
    print("[+]Identifying Virtual Machine's IP Address...")
    ip = os.popen("nmap -sn 192.168.1.0-255 | grep '"+netname+"'")
    ip = ip[42:len(ip)-2]
    print("Virtual Machine's IP Address identified ("+ip+")\n")
    return ip

def adb_connect():
    print("[+]Connecting to Virtual Machince using ADB...")
    output = os.popen("adb connect "+find_vm_ip()).readline()

    if output[:8] == "connected":
        print("ADB is now connected to Virtual Machine\n")
    else:
        print("There was an issue with connecting to the Virtual Machine")
        print(output+"\n")

def install_magisk():
    print("[+]Installing Magisk on Virtual Machine...")
    latest_version =  lastversion.has_update(repo = "topjohnwu/Magisk", current_version=0)
    output = os.popen("adb install -g Masgisk-v"+str(latest_version)+".apk")

def open_magisk():
    #open magisk on vm using tap adb commands