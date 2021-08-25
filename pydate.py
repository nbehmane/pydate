#!/usr/bin/python3
import subprocess
import invoke
import os

OS = 'ubuntu'

def get_w():
    """Another way of getting user information"""
    return subprocess.call("w > file", shell=True)

def users_active():
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
            return True
        idle_time = idle_time.replace(':', '')
        idle_time = idle_time.replace('.', '')
        # if the user has been idle for 10 minutes or longer
        if 'm' in idle_time:
            return True
        if 's' in idle_time:
            idle_time = idle_time.replace('s', '')
            if int(idle_time) >= 1000:
                return True
    return False

def check_return(ret, msg_p=None, msg_f=None):
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
    print(f"{79 * '-'}")
    print(msg)
    print(f"{79 * '-'}")

def main():
    active = users_active()
    if active == False:
        p_print("Skipping updates...Active users...")
    else:
        p_print("Beginning updates...")
        if OS == 'manjaro':
            ret = subprocess.call('pacman -Syu', shell=True)

        elif OS == 'ubuntu':
            # To add --> Check if a reboot is required for the update.
            # If it is required, cancel the upate and send an email
            # to notify that theres needs to be a manual update.
            # Otherwise continue the update.
            ret = subprocess.call('apt-get update', shell=True)


            if os.path.isfile("/var/run/reboot-required"):
                p_print("Reboot Required.")
                ret = 1;
            else:
                p_print("No reboot required...Updating...")
                ret = subprocess.call('inv run-ubuntu-update', shell=True)

        check_return(ret, "*** Done updating. ***", 
                "*** Update not completed. Check output. ***")


if __name__ == "__main__":
    main()


