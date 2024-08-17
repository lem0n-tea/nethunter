# gui.py
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from port_scanner import PortScanner
from port_parser import port_parse
from socket import gaierror


def perform_scan():
    # Get host and ports from entries
    target_host = host_entry.get()
    port_range = port_entry.get()
    if not target_host or not port_range:
        messagebox.showerror("Error", "Please enter a target host and a port range")
        return

    try:
        scanner = PortScanner(target_host)
        # Check if ports parsed properly
        ports = port_parse(port_range)
        if not isinstance(ports, list):
            messagebox.showerror("Error", ports)
            return

        # Scan ports on host
        open_ports = scanner.scan(ports)
    except gaierror:
        messagebox.showerror("Error", f"Invalid host - {target_host}")
        return
    except:
        messagebox.showerror("Error", f"Some error occured while trying to scan {target_host}")
        return

    # Construct output for scan results
    output = f'Scan report on {target_host}:\nPORT\tSTATE\n'
    for port in open_ports:
        output += f'{port}/tcp\topen\n'

    # Insert scan results
    scan_results.config(state=NORMAL)
    scan_results.delete(1.0, END)
    scan_results.insert(END, output)
    scan_results.config(state=DISABLED)


if __name__ == "__main__":
    root = Tk()
    root.title("NetHunter - Port Scan")
    root.geometry('360x500')

    title_label = ttk.Label(root, text="NetHunter", font=("Lucida Console", 18))
    title_label.pack(pady=10)

    host_prompt = ttk.Label(root, text="Host", font=("Lucida Console", 11))
    host_prompt.place(x=10, y=50, width=50, height=30)

    host_entry = ttk.Entry(root, font=("Lucida Console", 9))
    host_entry.place(x=60, y=50, width=200, height=30)
    host_entry.insert(0, "Enter IP or hostname")
    host_entry.bind("<FocusIn>", lambda args: host_entry.delete('0', 'end'))

    port_prompt = ttk.Label(root, text="Ports", font=("Lucida Console", 11))
    port_prompt.place(x=10, y=90, width=50, height=30)

    port_entry = ttk.Entry(root, font=("Lucida Console", 9))
    port_entry.place(x=60, y=90, width=200, height=30)
    port_entry.insert(0, "Enter port range")
    port_entry.bind("<FocusIn>", lambda args: port_entry.delete('0', 'end'))

    scan_button = ttk.Button(root, text="Scan", command=perform_scan)
    scan_button.place(x=270, y=50, width=80, height=70)

    results_label = ttk.Label(root, text="Scan Results", font=("Lucida Console", 14), anchor="c")
    results_label.place(x=0, y=130, width=360, height=20)

    scan_results = Text(root, wrap="word", state=DISABLED, font=("Lucida Console", 10))
    scan_results.place(x=5, y=160, width=325, height=300)

    ys = ttk.Scrollbar(orient="vertical", command=scan_results.yview)
    ys.place(x=330, y=160, width=25, height=300)
    scan_results["yscrollcommand"] = ys.set

    root.mainloop()
