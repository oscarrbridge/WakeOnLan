from bt_proximity import BluetoothRSSI
import time
import sys
import math

NUM_LOOP = 2

def print_usage():
    print "Usage: python test_address.py <bluetooth-address>"

def main():
    if len(sys.argv) > 1:
        addr = sys.argv[1]
    else:
        print_usage()
        return
    if len(sys.argv) == 3:
        num = int(sys.argv[2])
    else:
        num = NUM_LOOP
    btrssi = BluetoothRSSI(addr=addr)

    for i in range(1, num):
        rssi_bt = float(btrssi.get_rssi())        
        if rssi_bt == 0:
            print("i")
        else:
            print("o")
            



if __name__ == '__main__':
    main()