import socket
import json
import os
import concurrent.futures 

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
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET para IPv4, SOCK_STREAM para TCP
        sock.settimeout(self.timeout) #tiempo de espera del socket
        result = sock.connect_ex((self.target_ip, port)) #connect_ex devuelve 0 si el puerto está abierto
        sock.close()
        
        if result == 0: #si el puerto está abierto
            port_info = self.ports_db.get(str(port), {
                'name': 'unknown',
                'risk': 'unknown',
                'description': 'Unknown service'
            })
            
            return { #retorna un diccionario con la información del puerto
                'port': port,
                'state': 'open',
                'service': port_info['name'],
                'risk': port_info['risk'],
                'description': port_info['description']
            }
        else:
            return None
    
    def scan_ports(self, ports, max_threads=300):
        """
        Escanea múltiples puertos usando threading
        
        Args:
            ports: Lista de puertos a escanear
            max_threads: Número máximo de threads concurrentes
            
        Returns:
            Lista
        """
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            future_to_port = {executor.submit(self.scan_port, port): port for port in ports}
            for future in concurrent.futures.as_completed(future_to_port):
                result = future.result()
                if result:  # Solo agregar si el puerto está abierto
                    results.append(result)
        
        return sorted(results, key=lambda x: x['port'])
    
    def quick_scan(self):
        """Escaneo rápido de puertos comunes"""
        common_ports = [21, 22, 23, 25, 80, 443, 445, 3306, 3389, 8080]
        return self.scan_ports(common_ports)

    def full_scan(self):
        """Escaneo completo de puertos"""
        ports = range(1, 65535)
        return self.scan_ports(ports)

    def scan_range(self, start, end):
        """Escaneo de un rango de puertos"""
        ports = range(start, end + 1)
        return self.scan_ports(ports)
    
