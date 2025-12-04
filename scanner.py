# scanner.py
import argparse
from modules.port_scanner import PortScanner
from modules.ai_analyzer import AIAnalyzer
from utils.colors import Colors, print_banner

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='AI-Powered Port Scanner')
    parser.add_argument('target', help='Target IP or hostname')
    parser.add_argument('--api-key', help='Gemini API key')
    parser.add_argument('--quick', action='store_true', help='Quick scan (common ports only)')
    
    args = parser.parse_args()
    
    # TODO: Escanear puertos
    # TODO: Analizar con IA
    # TODO: Mostrar resultados
    
if __name__ == '__main__':
    main()