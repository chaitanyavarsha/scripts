#!/usr/bin/env python3
import argparse, subprocess, sys
from argparse import RawTextHelpFormatter
from shlex import split

def run(cmd):
    try:
        runCmd = subprocess.call(cmd, shell=True)
        return runCmd.decode('utf-8')
    except Exception as err:
        return "Error with command."

def print_command(cmd):
    print(cmd)
    run(cmd)


############################################################

def connect(host, user, password, connection):
    if connection == "sol":
        print_command("ipmitool -I lanplus -H "+host+" -U "+user+" -P "+password+" sol activate")
    elif connection == "mpro":
        print_command("ipmitool -I lanplus -H "+host+" -U "+user+" -P "+password+" sol activate usesolkeepalive instance=2 ")
    else:
        print ("Unknown connection type ")

# def disconnect()
# def action(host, user, password, action)

def main():
    
    des =  """
    The default USER -> admin 
                PASSWORD-> admin
    To overwirte this you can secify custom USER and PASSWORD

    List of actions: 
    bios - Sets the Boot Device to BIOS and powercycles the host.
    power_cycle - Power cycles the host.
    sdr - Print the Sensor data.
    sel - Print the SEL logs.
    
    List of connection type:
    sol    mpro     secpro

    """
    
    use_age = """
    Example for using this script:

    Connect to Mpro:
        ipmi_helper.py -H <BMC_ADDRESS> -C mpro

    Connect to SOL:
        ipmi_helper.py -H <BMC_ADDRESS> -C sol

    Boot to BIOS with custom user and password:
        ipmi_helper.py -H <BMC_ADDRESS> -U <USER> -P <PASSWORD> -A bios

    Power cycle a host with custom user and password:
        ipmi_helper.py -H <BMC_ADDRESS> -U <USER> -P <PASSWORD> -A power_cycle
    """

    end ="""
        Thank you for using this script ! 
            Made with  <3  by Chaitanya
    """
    
    class MyParser(argparse.ArgumentParser):
        def error(self, message):
            sys.stderr.write('error: %s\n' % message)
            self.print_help()
            sys.exit(2)
    
    parse = MyParser(description=des, usage=use_age, epilog=end, formatter_class=RawTextHelpFormatter)
    parse.add_argument("-H", "--host", help="This option is where you specify the BMC IP address", required=True)

    required_args = parse.add_mutually_exclusive_group(required=True)
    required_args.add_argument("-C", "--connect", help="This option is to connect to an instance")
    required_args.add_argument("-A", "--action", help="This option is to perform an action| Print help for list of actions")

    parse.add_argument("-U", "--user", help="This is to specify custom USER", default='admin')
    parse.add_argument("-P", "--pass", help="This is to specify custom PASSWORD", default='admin')
    # parse.add_argument("-", "--", help="")
    args = vars(parse.parse_args())
    
    host = args['host']
    connection = args['connect']
    action = args['action']
    user = args['user']
    password = args['pass']


    if connect:
        print("connecting: ")
        connect(host, user, password, connection)
    elif action:
        print(action)
        # action(host, user, password, action)


if __name__ =="__main__":
    main()