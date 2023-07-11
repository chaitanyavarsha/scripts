#!/usr/bin/env python3
import subprocess
import socket
from shlex import split

def run(cmd):
    try:
        runCmd = subprocess.check_output(split(cmd), stderr=subprocess.DEVNULL)
        return runCmd.decode('utf-8')
    except Exception as err:
        return "Error with command."

    
def getBios():
    biosinfo = run('dmidecode -t bios')
    for line in biosinfo.splitlines():
        if "Vendor" in line:
            bios_vendor = line.split(":")[1].strip()
        if "Version" in line:
            bios_version = line.split(":")[1].strip()
    if bios_version:
        return bios_vendor,bios_version
    else:
        return "BIOS info not found", "BIOS info not found"
    
def getBMC():
    bmcinfo = run('ipmitool mc info')
    for line in bmcinfo.splitlines():
        if "Firmware Revision" in line :
            bmc_version = line.split(":")[1].strip()
            return bmc_version
    return "BMC Info not found"

def getbaseboard():
    bmcinfo = run('ipmitool fru print 0')
    for line in bmcinfo.splitlines():
        if "Board Product" in line :
            bb_name = line.split(":")[1].strip()
            return bb_name
    return "Board product not found"

def ipBMC():
    lan_print = run('ipmitool lan print 1')
    for line in lan_print.splitlines():
        if "IP Address Source" not in line and "IP Address" in line:
            bmc_ip = line.split(":")[1].strip()
            return bmc_ip
    return "BMC IP not found"

def getSerial():
    dmidecode = run('dmidecode -t baseboard')
    for line in dmidecode.splitlines():
        if "Serial Number" in line:
            serial = line.split(":")[1].strip()
        # elif "Version" in line:
        #     bb_version = line.split(":")[1].strip()
    if serial:
        return serial 
    else:
        return "Base board info N/A", "Base board info N/A"
    return "Not Found"

def getManu():
    dmidecode = run('dmidecode -t chassis')
    for line in dmidecode.splitlines():
        if "Manufacturer" in line:
            manu = line.split(":")[1].strip()
            return manu
    return "Chassis info Not Found"

def getCpus():
    dmidecode = run('dmidecode -t processor')
    versions = []
    sockets = []
    part_numbs = ""
    
    for line in dmidecode.splitlines():
        if "Version:" in line:
            version = line.split(":")[1].strip()
            versions.append(version)
        elif "Socket Designation:" in line:
            socket = line.split(":")[1].strip()
            sockets.append(socket)
        elif "Part Number" in line:
            part_num = line.split(":")[1].strip()
            part_numbs += "{} |".format(part_num)
    if len(versions) == len(sockets):
        uniqversions = len(set(versions)) == 1
        if uniqversions:
            countversions = "{} x {}".format(len(versions), versions[0])
            return countversions, part_numbs[:-1]
        else:
            return "CPUs are different"
    else:
        return "CPU Count Error"
    return "CPU Not found Error"

def getDIMMs():
    dmidecode = run('dmidecode -t memory')
    dimms = []
    for dimm in dmidecode.split("Memory Device"):
        size = ""
        manu = ""
        partnumber = ""
        for info in dimm.splitlines():
            if  'Size:' in info and "No" not in info:
                if "Volatile" not in info:
                    size = info.split(":")[1].strip()
            elif "Manufacturer:" in info and "NO" not in info:
                manu = info.split(":")[1].strip()
            elif "Part Number:" in info and "NO" not in info :
                partnumber = info.split(":")[1].strip()
        if len(size):
            dimms.append([size, manu, partnumber])

    dimm_str = ""
    for each_dimm in dimms:
            dimm_str = set(each_dimm)
    list_of_strings = [str(s) for s in dimm_str]
    joined_string = " ".join(list_of_strings)
    dimm_info = " x ".join([format(len(dimms)), joined_string])
    if dimm_info:
        return dimm_info
    else:
        return "DIMM info not found"

def getDisks():
    lsblk = run('lsblk -dno TRAN,SIZE,MODEL')
    lines = lsblk.splitlines()
    no_disks = {i:lines.count(i) for i in lines}
    final_disks = " | ".join('{} x {}'.format(*p).strip() for p in no_disks.items())
    if final_disks:
        return final_disks
    else:
        return "Disks info not found"

def getNics():
    lspci = run('lspci')
    models = ""
    for line in lspci.splitlines():
        if "Ethernet" in line:
            model = line.split(":").pop().strip()
            models += "{} | ".format(model)
    if models:
        return models
    else:
        return "NIC info not found"

#####################################  MAIN
run('hostname AEhost')
hostname = "AEhost"
IPAddr = socket.gethostbyname(hostname)
serial = getSerial()
baseboard = getbaseboard()
manufacturer = getManu()
cpus, part = getCpus()
dimm_info = getDIMMs()
# disks = getDisks()
# nics = getNics()
bios_vendor, bios_version = getBios()
bmc_version = getBMC()
bmc_address = ipBMC()
print("Hostname:  " + hostname)
print("Serial:  " + serial)
print("Base board Version: "+ baseboard)
print("Manu: " + manufacturer)
print("CPU info: " + cpus)
print("CPU part numbers: " + part)
print("DIMMS Info: "+ dimm_info)
# print("HDD info: "+ disks)
# print("NIC info :"+ nics)
# print("BIOS Vendor: " + bios_vendor ) 
print("BIOS Info: "+ bios_vendor + " | "+ bios_version)
print("BMC Info: " + bmc_version)
print("Host IP: "+ IPAddr)
print("BMC IP address: " + bmc_address)

