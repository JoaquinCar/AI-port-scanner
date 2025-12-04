import google.generativeai as genai
import json
import os

class AIAnalyzer:
    def __init__(self, api_key=None):
        """
        Inicializa el analizador IA
        
        Args:
            api_key: Gemini API key (o usar variable de entorno GEMINI_API_KEY)
        """
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("Gemini API key required")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def analyze_port_scan(self, scan_results, target):
        """
        Analiza un resultado de escaneo de puertos
        """
        prompt = f"""You are a senior cybersecurity engineer performing threat assessment. Analyze this port scan with precision.

TARGET: {target}
SCAN RESULTS:
{json.dumps(scan_results, indent=2)}

Provide technical analysis in valid JSON (no markdown):
{{
  "risk_score": <integer 0-10>,
  "severity": "<critical|high|medium|low>",
  "critical_findings": [
    {{
      "port": <int>,
      "service": "<name>",
      "vulnerability": "<specific CVE or weakness>",
      "exploit_likelihood": "<high|medium|low>",
      "impact": "<brief technical impact>"
    }}
  ],
  "attack_vectors": [
    "<specific attack technique with port number>"
  ],
  "immediate_actions": [
    "<prioritized remediation step>"
  ],
  "reconnaissance_notes": "<what this reveals about the target infrastructure>"
}}

Rules:
- Only include ports with actual security implications
- Reference specific CVEs when applicable
- Prioritize by exploitability and impact
- No generic advice - be surgical
- If score >= 8, it must be immediately actionable critical risk
- Focus on what an attacker would exploit first
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # Limpiar markdown si existe
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            
            return json.loads(text.strip())
            
        except Exception as e:
            return {
                "risk_score": 0,
                "severity": "error",
                "critical_findings": [],
                "attack_vectors": [],
                "immediate_actions": [f"Error analyzing results: {str(e)}"],
                "reconnaissance_notes": "Analysis failed."
            }


