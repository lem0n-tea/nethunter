# port_scanner.py
import socket
import threading
from queue import Queue


class PortScanner:
    def __init__(self, target, timeout=1, workers_count=500):
        # Determine scan target, socket timeout and max count of threads
        self.target_ip = socket.gethostbyname(target)
        self.timeout = timeout
        self.workers_count = workers_count
        self.print_lock = threading.Lock()

    def scan(self, ports):
        # Scan a range of ports on a specified target host
        open_ports = []
        port_queue = Queue()

        # Task that each thread performs
        def threader():
            while True:
                # Gets port number from the queue and if it is open on host, adds it to the list
                port_number = port_queue.get()
                if self.is_port_open(port_number):
                    with self.print_lock:
                        open_ports.append(port_number)
                port_queue.task_done()

        # Create a pool of worker threads
        for _ in range(self.workers_count):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()

        # Add ports to the queue
        for port in ports:
            port_queue.put(port)

        # Wait for all tasks to complete
        port_queue.join()

        return open_ports

    def is_port_open(self, port):
        # Initializes a TCP connection to a specified target
        try:
            socket.setdefaulttimeout(self.timeout)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            con = s.connect_ex((self.target_ip, port))
            s.close()
            return con == 0
        except Exception:
            return False
