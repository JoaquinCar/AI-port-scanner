import argparse
import os
from dotenv import load_dotenv
from modules.port_scanner import PortScanner
from modules.ai_analyzer import AIAnalyzer
from utils.colors import Colors, print_banner

# Cargar variables de entorno
load_dotenv()

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='AI-Powered Port Scanner')
    subparsers = parser.add_subparsers(dest='command')
    
    # Scan subcommand
    scan_parser = subparsers.add_parser('scan', help='Scan ports on a target')
    scan_parser.add_argument('-t', '--target', required=True, help='Target IP or hostname')
    scan_parser.add_argument('-a', '--analyze', action='store_true', help='Enable AI analysis')
    scan_parser.add_argument('-q', '--quick', action='store_true', help='Quick scan (common ports)')
    scan_parser.add_argument('-r', '--range', help='Port range (e.g., 1-100)')
    scan_parser.add_argument('-p', '--port', type=int, help='Scan single port')
    scan_parser.add_argument('-f', '--full', action='store_true', help='Full scan (all 65535 ports)')
    
    args = parser.parse_args()

    if args.command == 'scan':
        print(f"\n{Colors.CYAN}Scanning {args.target}...{Colors.RESET}\n")
        
        scanner = PortScanner(args.target)
        
        # Determinar tipo de scan
        if args.port:
            result = scanner.scan_port(args.port)
            results = [result] if result else []
        elif args.range:
            start, end = map(int, args.range.split('-'))
            results = scanner.scan_range(start, end)
        elif args.full:
            results = scanner.full_scan()
        else:
            results = scanner.quick_scan()
        
        # Mostrar resultados basicos
        print(f"{Colors.GREEN}Found {len(results)} open ports:{Colors.RESET}\n")
        for r in results:
            risk_color = Colors.RED if r['risk'] == 'critical' else Colors.YELLOW if r['risk'] == 'high' else Colors.WHITE
            print(f"  {r['port']}/tcp - {r['service']} [{risk_color}{r['risk']}{Colors.RESET}]")
        
        # Analisis IA (solo si se pasa flag -a)
        if args.analyze:
            if not results:
                print(f"\n{Colors.YELLOW}No open ports to analyze.{Colors.RESET}\n")
            else:
                api_key = os.getenv('GEMINI_API_KEY')
                if not api_key:
                    print(f"\n{Colors.RED}Error: GEMINI_API_KEY not found in environment{Colors.RESET}")
                    print(f"Set it in .env file or export GEMINI_API_KEY=your_key\n")
                else:
                    print(f"\n{Colors.CYAN}AI Analysis in progress...{Colors.RESET}\n")
                    
                    analyzer = AIAnalyzer(api_key=api_key)
                    analysis = analyzer.analyze_port_scan(results, args.target)
                    
                    if analysis:
                        print_ai_analysis(analysis)
        elif not results:
            print(f"\n{Colors.YELLOW}No open ports found.{Colors.RESET}\n")
    else:
        parser.print_help()

def print_ai_analysis(analysis):
    """Imprime analisis IA"""
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}AI SECURITY ANALYSIS{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    
    # Risk Score
    score = analysis.get('risk_score', 0)
    severity = analysis.get('severity', 'unknown')
    print(f"{Colors.BOLD}Risk Score:{Colors.RESET} {score}/10 [{severity.upper()}]\n")
    
    # Critical Findings
    findings = analysis.get('critical_findings', [])
    if findings:
        print(f"{Colors.BOLD}Critical Findings:{Colors.RESET}")
        for f in findings:
            print(f"  Port {f['port']} ({f['service']})")
            print(f"    - {f['vulnerability']}")
            print(f"    - Likelihood: {f['exploit_likelihood']}")
            print(f"    - Impact: {f['impact']}\n")
    
    # Attack Vectors
    vectors = analysis.get('attack_vectors', [])
    if vectors:
        print(f"{Colors.BOLD}Attack Vectors:{Colors.RESET}")
        for v in vectors:
            print(f"  - {v}")
        print()
    
    # Immediate Actions
    actions = analysis.get('immediate_actions', [])
    if actions:
        print(f"{Colors.BOLD}Immediate Actions:{Colors.RESET}")
        for i, a in enumerate(actions, 1):
            print(f"  {i}. {a}")
        print()
    
    # Recon Notes
    notes = analysis.get('reconnaissance_notes', '')
    if notes:
        print(f"{Colors.BOLD}Reconnaissance Notes:{Colors.RESET}")
        print(f"  {notes}\n")
    
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

if __name__ == '__main__':
    main()