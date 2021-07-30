import os
import time
from wakeonlan import send_magic_packet

BLUETOOTH_MAC = "3C:F7:A4:0A:38:7A 10"
NUMBER_OF_PINGS = 1

pc_on = False

counter = 0
time_in_range = [0, 0, 0]

def check_pc_stat():
    final = ""
     
    os.system("ping 192.168.1.36 -c 1 > ping.txt")
    with open("ping.txt", "r") as ping_txt:
        all_lines = ping_txt.readlines()
        x = all_lines[4].split(",")
        try:    
            final = x[1][1]
        except IndexError:
            return False
    if final == 0:
        return False
    else:
        return True
        
        

def check_time_in_range(count):
    global counter, time_in_range, pc_on
    
    if counter == 3:
        counter = 0
    
    time_in_range[counter] = count
    counter += 1
    
    total_time = (time_in_range[0] + time_in_range[1] + time_in_range[2])
    
    return total_time

def check_for_range():
    os.system("python lnsm.py {} {} > blue.txt".format(BLUETOOTH_MAC, NUMBER_OF_PINGS))
    
    total_lines = 0

    with open('blue.txt', 'r') as pings_txt:
        all_text = pings_txt.readlines()
        
    x = all_text[0].split("\n")
    final_text = x[0]

    if final_text == "i":
        return 1
        
    else:
        return 0
    
def main():
    global pc_on
    while True:
        times_counted = check_time_in_range(check_for_range())
        if times_counted == 3:
            print("sent magic packet")
            send_magic_packet("24:4B:FE:58:5F:FA")
            pc_on = True
            while pc_on is True:    
                pc_on = check_pc_stat()
                time.sleep(600)
        print("checked_range", times_counted)
        time.sleep(3)


if __name__ == "__main__":
    main()
