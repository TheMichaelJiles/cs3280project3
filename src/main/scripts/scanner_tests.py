import unittest
import socket
from cs3280project3 import scan

class ScannerTest(unittest.TestCase):
    def test_one_port_open(self):
        sock = socket.socket()
        sock.bind(('127.0.0.1', 4001))
        sock.listen(5)
        port_dict = scan('127.0.0.1', 4001, 4002)
        correct_dict = {
            4001 : True
        }
        sock.close()
        self.assertEqual(port_dict, correct_dict)

    def test_10_ports_open(self):
        socks = []
        ports = [50001, 50002, 50003, 50004, 50005, 50006, 50007, 50008, 50009, 50010]
        correct_dict = {}

        for port in ports:
            sock = socket.socket()
            sock.bind(('127.0.0.1', port))
            sock.listen(5)
            correct_dict[port] = True
            socks.append(sock)

        port_dict = scan('127.0.0.1', 50001, 50011)
        for sock in socks:
            sock.close()
        self.assertEqual(port_dict, correct_dict)

    def test_10_ports_closed(self):
        ports = [50001, 50002, 50003, 50004, 50005, 50006, 50007, 50008, 50009, 50010]
        correct_dict = {}

        for port in ports:
            correct_dict[port] = False

        port_dict = scan('127.0.0.1', 50001, 50011)
        self.assertEqual(port_dict, correct_dict)

if __name__ == '__main__':
    unittest.main()
