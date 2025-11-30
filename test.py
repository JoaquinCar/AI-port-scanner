# test.py
from modules.port_scanner import PortScanner

scanner = PortScanner('scanme.nmap.org')
result = scanner.scan_port(22)
print(result)
