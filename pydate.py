#!/usr/bin/python3
from time import localtime
import subprocess
import invoke
import os


OS = 'ubuntu'

def get_w():
    """Another way of getting user information"""
    return subprocess.call("w > file", shell=True)

def users_active():
    """Checks if there are any users active on the system."""

    # grab the current users and information about them
    ret = get_w()
    f = open("file", "r")
    result = []
    for line in f:
        result.append(line.split())
    f.close()
    subprocess.call("rm file", shell=True)

    for user_index in range(2, len(result)):
        idle_time = result[user_index][4]
        user_name = result[user_index][0]
        print(f'{user_name} | {idle_time}')
        if user_name == 'ee-helpd':
            return False
        idle_time = idle_time.replace(':', '')
        idle_time = idle_time.replace('.', '')
        # if the user has been idle for 10 minutes or longer
        if 'm' in idle_time:
            return False
        if 's' in idle_time:
            idle_time = idle_time.replace('s', '')
            if int(idle_time) >= 1000:
                return False
    return True

def check_return(ret, msg_p=None, msg_f=None):
    """Check the return code, and print a pass or fail message"""

    if ret == 0 and msg_p == None:
        return True
    elif ret == 0 and msg_p != None:
        p_print(msg_p)
        return True
    elif ret > 0 and msg_f == None:
        return False
    elif ret > 0 and msg_f != None:
        p_print(msg_f)
        return False

def p_print(msg):
    """pretty print a message."""
    print(f"{79 * '-'}")
    print(msg)
    print(f"{79 * '-'}")

def main():
    active = users_active()
    time = localtime()

    time_on = f"Time Initiated: {time[3]}:{time[4]}:{time[5]}"
    subprocess.call(f"echo {time_on} 2>&1 | tee -a upgrade_log", shell=True)

    if active == True:
        p_print("Skipping updates...Active users...")
    else:
        p_print("Beginning updates...")
        if OS == 'manjaro':
            ret = subprocess.call('pacman -Syu', shell=True)

        elif OS == 'ubuntu':
            ret = subprocess.call('apt-get update 2>&1 | tee -a upgrade_log', shell=True)
            if os.path.isfile("/var/run/reboot-required"):
                p_print("Reboot Required.")
                ret = 1
            else:
                p_print("No reboot required...Updating...")
                ret = subprocess.call("inv -r '/home/ee-helpdesk/pydate/pydate' run-ubuntu-update 2> out", shell=True)
        check_return(ret, "*** Done updating. ***", 
                "*** Update not completed. Check output. ***")

if __name__ == "__main__":
    main()


