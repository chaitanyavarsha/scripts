from shlex import split
import subprocess, argparse


# modprobe einj
# echo 0 > /sys/kernel/debug/apei/einj/param1
# echo  0xfffffffffffff000 > /sys/kernel/debug/apei/einj/param2
# echo 0x8 > /sys/kernel/debug/apei/einj/error_type
# echo 1 > /sys/kernel/debug/apei/einj/error_inject 


def run(cmd):
    try:
        runCmd = subprocess.check_output(split(cmd), stderr=subprocess.DEVNULL)
        return runCmd.decode('utf-8')
    except Exception as err:
        return "Error with command."

def init():
    # run('modprobe einj')
    print("modprobe einj")

def error_type(error_name):
    if not error_name:
        print("Type undefined Going default")
        print("echo\"0x8\" > /sys/kernel/debug/apei/einj/error_type")
    elif error_name == "UE":
        print("echo\"0x10\" > /sys/kernel/debug/apei/einj/error_type")
    else:
        print("echo\"0x8\" > /sys/kernel/debug/apei/einj/error_type")

def vendor_flag(flag=False):
    if flag == True:
        print("echo 1 > /sys/kernel/debug/apei/einj/vendor_flags")
    else:
        print("Skipping vendor flag")


def main():
    # print ("Initializing EINJ")
    init()
    ap = argparse.ArgumentParser()
    error_mods ="""
    Processing Element(PE), Memory Controller Unit (MCU)
    Coherent Mesh Interconnect (CMI), On-Chip Memory (OCM)
    """
    ap.add_argument("-F", "--vendor_flag", help="Option to turn on vendor flag", action="store_true")
    ap.add_argument("-t", "--type", help="CE or UE")
    args = vars(ap.parse_args())
    error_type(args['type'])
    vendor_flag(flag=args['vendor_flag'])

if __name__ == "__main__":
    main()