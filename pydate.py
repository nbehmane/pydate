#!/usr/bin/python3
import psutil
import subprocess

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

    for user_index in range(2, len(result)):
        idle_time = result[user_index][4]
        user_name = result[user_index][0]
        print(f'{user_name} | {idle_time}')
        if user_name == 'ee-helpd':
            continue
        if '.' in idle_time:
            return False
        idle_time = idle_time.replace(':', '')
        # if the user has been idle for 10 minutes or longer
        if int(idle_time) >= 1000:
            return True


def main():
    active = users_active()
    if active == False:
        print("Skipping updates...")
    else:
        print("Beginning updates...")
        ret = subprocess.call('apt-get update', shell=True)
        if ret == 0:
            print('Gathered update list...')
        elif ret > 0:
            print('Error occured. Aborting...')




if __name__ == "__main__":
    main()


