# scanner.py
import argparse
from modules.port_scanner import PortScanner
from modules.ai_analyzer import AIAnalyzer
from utils.colors import Colors, print_banner

def main():
    print_banner()
    #principal parser
    parser = argparse.ArgumentParser(description='AI-Powered Port Scanner')
    #subparser
    subparsers = parser.add_subparsers(dest='command')
    
    #parser para el escaneo
    scan_parser = subparsers.add_parser('scan', help='Scan ports on a target')

    scan_parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    scan_parser.add_argument('-k', '--api-key', help='Gemini API key')
    scan_parser.add_argument('-q', '--quick', action='store_true', help='Quick scan (common ports only)')
    scan_parser.add_argument('-r', '--range', type=int, help='Port range to scan (e.g., 1-100)')
    scan_parser.add_argument('-f', '--full', action='store_true', help='Full scan (all ports)')
    scan_parser.add_argument('-s', '--scan', type=int, help='Scan one port')
    scan_parser.add_argument('-i', '--resolve-ip', action='store_true', help='Resolve IP address')
    
    args = parser.parse_args()
    
    # TODO: Escanear puertos
    # TODO: Analizar con IA
    # TODO: Mostrar resultados
    
if __name__ == '__main__':
    main()