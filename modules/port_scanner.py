import socket
import json
import os

class PortScanner:
    def __init__(self, target, timeout=1):
        self.target = target
        self.timeout = timeout
        try:
            self.target_ip = self.resolve_target()
        except socket.gaierror:
            raise ValueError(f"Cannot resolve {target}")
        
        # Calculate absolute path to data file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'common_ports.json')
        
        # Cargar JSON
        with open(data_path, 'r') as f:
            data = json.load(f)
            self.ports_db = {**data['tcp'], **data['udp'], **data['malware']}
    
    def resolve_target(self):
        """Convierte hostname a IP"""
        ip = socket.gethostbyname(self.target)
        return ip
    
    def scan_port(self, port):
        """Escanea un puerto"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        result = sock.connect_ex((self.target_ip, port))
        sock.close()
        
        if result == 0:
            port_info = self.ports_db.get(str(port), {
                'name': 'unknown',
                'risk': 'unknown',
                'description': 'Unknown service'
            })
            
            return {
                'port': port,
                'state': 'open',
                'service': port_info['name'],
                'risk': port_info['risk'],
                'description': port_info['description']
            }
        else:
            return None