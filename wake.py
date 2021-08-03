import os
import time
from wakeonlan import send_magic_packet

PC_MAC = "24:4B:FE:58:5F:FA"
BLUETOOTH_MAC = "3C:F7:A4:0A:38:7A"
PC_IP = "192.168.1.36"
NUMBER_OF_PINGS = 1

pc_on = False

counter = 0
time_in_range = [0, 0, 0]
total_time = 0


def check_pc_stat():
     
    os.system("ping {} -c 1 > ping.txt".format(PC_IP))
    with open("ping.txt", "r") as ping_txt:
        all_lines = ping_txt.readlines()

    try:
        received = all_lines[4].split(",")
        for letter in received[1]:
            if letter == "1":
                print("Pinged computer on")
                return True
                
            if letter == "0":
                print("Pinged computer off")
                return False
    except IndexError:
        print("Pinged computer off")
        return False


def check_time_in_range(count):
    global counter, time_in_range, pc_on, total_time
    
    time_in_range = [0, 0, 0]
    
    if counter == 3:
        counter = 0
    
    time_in_range[0] = count
    counter += 1
    
    try:    
        total_time = (time_in_range[0] + time_in_range[1] + time_in_range[2])
    except TypeError:
        print("some stupid bug")
    
    print(time_in_range)
    
    return total_time


def check_for_range():
    os.system("python lnsm.py {} > blue.txt".format(BLUETOOTH_MAC))
    letter_check = []

    with open('blue.txt', 'r') as pings_txt:
        all_text = pings_txt.readlines()
    for letter in all_text:
        letter_check.append(letter)
    if "i\n" in letter_check:
        return 1
    else:
        return 0


def main():
    global pc_on, time_in_range
    running = 0
    print("Checking")
    while True:
        times_counted = check_time_in_range(check_for_range())
        if times_counted >= 1:
            print("sent magic packet")
            send_magic_packet(PC_MAC)
            pc_on = True
            while pc_on is True:    
                pc_on = check_pc_stat()
                time.sleep(3)
                running += 3
                print(running)
                
        time_in_range = [0, 0, 0]
        running += 3
        print(running)
        
        time.sleep(3)


if __name__ == "__main__":
    main()
