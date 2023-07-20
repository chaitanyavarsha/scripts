#!/usr/bin/env python3

from shlex import split
import subprocess, argparse, sys
from argparse import RawTextHelpFormatter
from time import sleep



class ErrorToInject:
    def __init__(self, param1, param2, error_type, vendor_flag):
        self.param1 = param1 
        self.param2 = param2
        self.error_type = error_type
        self.vendor_flag = vendor_flag

### Init_ ###
    def init(self):
        return "modprobe einj"

    def init_param1(self, param1):
        param = "echo "+param1+" > /sys/kernel/debug/apei/einj/param1"
        return param

    def init_param2(self, param2):
        if not param2:
            param2="0xfffffffffffff000"
        param = "echo "+param2+" > /sys/kernel/debug/apei/einj/param2"
        return param

    def init_vendor_flag(self):
        param = "echo 0x1 > /sys/kernel/debug/apei/einj/vendor_flags"
        return param


    def init_error_type(self, error_name):
        if error_name == "UE":
            param = "echo 0x10 > /sys/kernel/debug/apei/einj/error_type"
        else:
            param = "echo 0x8 > /sys/kernel/debug/apei/einj/error_type"
        return param



#### Actions ###

    def run(self, cmd):
        try:
            runCmd = subprocess.call(cmd, shell=True, stderr=subprocess.DEVNULL)
            return runCmd.decode('utf-8')
        except Exception as err:
            return "Error with command."

    def inject(self, count):
        self.run(self.init())
        self.run(self.init_param1(self.param1))
        self.run(self.init_param2(self.param2))
        self.run(self.init_error_type(self.error_type))
        print("Injecting error(s)")
        self.verify()
        if self.vendor_flag:
            self.run(self.init_vendor_flag())
        for i in range(count):
            self.run("echo 1 > /sys/kernel/debug/apei/einj/error_inject")

    def verify(self):
        print(self.init())
        print(self.init_param1(self.param1))
        print(self.init_param2(self.param2))
        print(self.init_error_type(self.error_type))
        if self.vendor_flag:
            print(self.init_vendor_flag())
        print("echo 1 > /sys/kernel/debug/apei/einj/error_inject")
    


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
    
    ### Default Error Injection ###

    if args['default_err']:
        default_err_inject(args['default_err'], print_flag, count)

    ### Custom Error Injection ###
    e = ErrorToInject(custom_address1, custom_address2, error_type_flag, vendor_flag)
    
    if print_flag:
        e.verify()
    else:
        e.inject(count)

if __name__ == "__main__":
    main()