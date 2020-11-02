#! /usr/bin/python
'''
Port Scanner
'''
__author__ = "Michael Jiles"
__version__ = "Fall 2020"
import multiprocessing
import socket
import sys

def scan(ip_address, start_port, end_port):
    '''
    Scans the passed in range of ports and creates a
    dictionary of ports and whether or not they are open
    '''
    proc_list = []
    port_dict = {}
    receiver, sender = multiprocessing.Pipe()

    for val, port in enumerate(range(start_port, end_port), 1):
        proc = multiprocessing.Process(name=(
            '#Proc'+str(val)), target=scan_single_port, args=(ip_address, port, sender))
        proc.start()
        proc_list.append(proc)

    for port in range(start_port, end_port):
        port_pair = receiver.recv()
        port_dict[port_pair[0]] = port_pair[1]

    for proc in proc_list:
        proc.join()

    return port_dict


def scan_single_port(ip_address, port, sender):
    '''
    Scans a single port and sends a value from the sender for whether or not the port is open
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = sock.connect_ex((ip_address, port))
    if response == 0:
        sender.send([port, True])
    else:
        sender.send([port, False])
    sock.close()

if __name__ == "__main__":
    ip = sys.argv[1]
    start = int(sys.argv[2])
    if len(sys.argv) == 4:
        end = int(sys.argv[3])
        print(scan(ip, start, end + 1))
    else:
        print(scan(ip, start, start + 1))
