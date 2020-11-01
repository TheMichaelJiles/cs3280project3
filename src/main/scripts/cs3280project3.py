#! /usr/bin/python
import multiprocessing
import socket
import sys

def scan(ip_address, start_port, end_port):
    proc_list = []
    port_dict = {}
    receiver, sender = multiprocessing.Pipe()
    print(ip_address)

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response = sock.connect_ex((ip_address, port))
    print(response)
    if response == 0:
        sender.send([port, True])
    else:
        sender.send([port, False])
    sock.close()

if __name__ == "__main__":
    ip = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    print(scan(ip, start, end))
