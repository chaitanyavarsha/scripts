#!/usr/bin/env python3

from shlex import split
import subprocess, argparse, sys
from argparse import RawTextHelpFormatter
from time import sleep

################################## ACTIONS ##########################

def run(cmd):
    try:
        runCmd = subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL)
        return runCmd.decode('utf-8')
    except Exception as err:
        return "Error with command."

def print_command(cmd, print_flag=False):
    if print_flag:
        print(cmd)
        # run(cmd)
    else:
        run(cmd)
        sleep(0.5)


################################# SETUP ##############################

def init(print_flag):
    print_command("modprobe einj", print_flag)

def param1(print_flag, custom_address1):
    print_command("echo  "+custom_address1+" > /sys/kernel/debug/apei/einj/param1", print_flag)

def param2(print_flag, custom_address2):
    if not custom_address2:
        custom_address2="0xfffffffffffff000"
    print_command("echo  "+custom_address2+" > /sys/kernel/debug/apei/einj/param2", print_flag)

def vendor_flag_check(print_flag, flag=False):
    if flag == True:
        print_command("echo 0x1 > /sys/kernel/debug/apei/einj/vendor_flags", print_flag)


def error_type(print_flag, error_name):
    if not error_name:
        print_command("echo 0x8 > /sys/kernel/debug/apei/einj/error_type", print_flag)
    elif error_name == "UE":
        print_command("echo 0x10 > /sys/kernel/debug/apei/einj/error_type", print_flag)
    else:
        print_command("echo 0x8 > /sys/kernel/debug/apei/einj/error_type", print_flag)

############################# Default_ERR_Directory #########################
# def default_err_inject(error_to_inject):
#     dict error_mods = {}


############################### INJECT #################################
def inject(print_flag, custom_address1, custom_address2, error_type_flag, vendor_flag):
    init(print_flag)
    param1(print_flag, custom_address1)
    param2(print_flag, custom_address2)
    vendor_flag_check(print_flag, vendor_flag)
    error_type(print_flag, error_type_flag)
    print_command("echo 1 > /sys/kernel/debug/apei/einj/error_inject", print_flag)

def main():
    end = '''
    Example usage:

        Inject CE error with custom adderss:
            python3 error_injection.py -C1 <ADDRESS> 
        
        Inject with Vendor_Flag activated:
            python3 error_injection.py -F -C1 <ADDRESS>

        Inject UE with custome address:
            python3 error_injection.py -C1 -t UE

        Injeciton same error multiple times:
            python3 error_injection.py -C1 <ADDRESS> -c <NUMBER>
        
        Print the commands used for injecting the error: 
            python3 error_injection.py -C1 <ADDRESS> -v 
    
        Thank you for using this script ! 
            Made with  <3  by Chaitanya
    '''
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)

    ap = MyParser(epilog=end,formatter_class=RawTextHelpFormatter)
    error_mods ="""
    Follwing are the default RAS error mods
    Processing Element(PE), Memory Controller Unit (MCU)
    Coherent Mesh Interconnect (CMI), On-Chip Memory (OCM)
    """
    
    ap.add_argument("-v","--verify",help="This prints the commands and runs them", action="store_true")
    ap.add_argument("-D", "--default_err", help=error_mods)
    ap.add_argument("-C1","--custom1",help="This maps to param1, can be used to inject custom error")
    ap.add_argument("-C2","--custom2",help="This maps to param2, can be used to inject custom error")
    ap.add_argument("-F", "--vendor_flag", help="Option to turn on vendor flag", action="store_true")
    ap.add_argument("-t", "--type", help="CE or UE")
    ap.add_argument("-c", "--count", help="Specify this option to inject multiple instances of a RAS error")
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
    default_err = args['default_err']
    count = 1 
    if args['count']:
        count = int(args['count'])

    if not (args['custom1'] or args['default_err']):
        ap.error("No Error specified for injection -D [MOD] -C1 <address> ")
    
    if args['default_err']:
        if count:
            for i in range(count):
                default_err_inject(args['default_err'])
    if count:
        for i in range(count):
            inject(print_flag, custom_address1, custom_address2, error_type_flag, vendor_flag)

if __name__ == "__main__":
    main()