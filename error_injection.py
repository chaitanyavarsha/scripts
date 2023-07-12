from shlex import split
import subprocess, argparse
from time import sleep

################################## ACTIONS ##########################

def run(cmd):
    try:
        runCmd = subprocess.check_output(split(cmd), stderr=subprocess.DEVNULL)
        return runCmd.decode('utf-8')
    except Exception as err:
        return "Error with command."

def print_command(cmd, print_flag=False):
    if print_flag:
        print(cmd)
        print("& run: "+cmd)
        sleep(1)
        # run(cmd)
    else:
        print(cmd)

################################# SETUP ##############################

def init(print_flag):
    print_command("modprobe einj", print_flag)

def param1(print_flag, custom_address1):
    print_command("echo  \""+custom_address1+"\" > /sys/kernel/debug/apei/einj/param1", print_flag)

def param2(print_flag, custom_address2):
    if not custom_address2:
        custom_address2="0xfffffffffffff000"
    print_command("echo  \""+custom_address2+"\" > /sys/kernel/debug/apei/einj/param2", print_flag)

def vendor_flag_check(print_flag, flag=False):
    if flag == True:
        print_command("echo 1 > /sys/kernel/debug/apei/einj/vendor_flags", print_flag)
    else:
        print("Skipping vendor flag")

def error_type(print_flag, error_name):
    if not error_name:
        print("Type undefined Going default")
        print_command("echo\"0x8\" > /sys/kernel/debug/apei/einj/error_type", print_flag)
    elif error_name == "UE":
        print_command("echo\"0x10\" > /sys/kernel/debug/apei/einj/error_type", print_flag)
    else:
        print_command("echo\"0x8\" > /sys/kernel/debug/apei/einj/error_type", print_flag)


############################### INJECT #################################
def inject(print_flag, custom_address1, custom_address2, error_type_flag, vendor_flag):
    init(print_flag)
    param1(print_flag, custom_address1)
    param2(print_flag, custom_address2)
    vendor_flag_check(print_flag, vendor_flag)
    error_type(print_flag, error_type_flag)
    print_command("echo 1 > /sys/kernel/debug/apei/einj/error_inject")

def main():
    ap = argparse.ArgumentParser()
    error_mods ="""
    Follwing are the default RAS error mods
    Processing Element(PE), Memory Controller Unit (MCU)
    Coherent Mesh Interconnect (CMI), On-Chip Memory (OCM)
    """
    
    ap.add_argument("-v","--verify",help="This prints the commands and runs them", action="store_true")
    ap.add_argument("-D", "--default_err", help=error_mods)
    ap.add_argument("-C1","--custom1",help="This maps to param1, can be used to inject custom error",required=True)
    ap.add_argument("-C2","--custom2",help="This maps to param2, can be used to inject custom error")
    ap.add_argument("-F", "--vendor_flag", help="Option to turn on vendor flag", action="store_true")
    ap.add_argument("-t", "--type", help="CE or UE")
    args = vars(ap.parse_args())
    
# modprobe einj
# echo 0 > /sys/kernel/debug/apei/einj/param1
# echo  0xfffffffffffff000 > /sys/kernel/debug/apei/einj/param2
# echo 0x8 > /sys/kernel/debug/apei/einj/error_type
# echo 1 > /sys/kernel/debug/apei/einj/error_inject 

    print_flag = args['verify']
    custom_address1 = args['custom1']
    custom_address2 = args['custom2']
    error_type_flag = args['type']
    vendor_flag = args['vendor_flag']


    inject(print_flag, custom_address1, custom_address2, error_type_flag, vendor_flag)

if __name__ == "__main__":
    main()