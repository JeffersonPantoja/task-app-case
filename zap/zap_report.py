import urllib.request
import urllib.parse
import json
import sys

ZAP_URL = "http://127.0.0.1:8090"

def rpc_call(url, data=None):
    headers = {}
    if data:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Erro na chamada da API ({url}): {e}")
        sys.exit(1)

def generate_report():
    print("Solicitando geração do relatório HTML ao ZAP...")
    api_url = f"{ZAP_URL}/JSON/reports/action/generate/"
    params = urllib.parse.urlencode({
        "title": "DAST Scan Report",
        "template": "traditional-html",
        "reportDir": "/zap/wrk",
        "reportFile": "zap-report.html"
    }).encode()
    
    res = rpc_call(api_url, data=params)
    print(f"Relatório gerado com sucesso: {res}")

if __name__ == "__main__":
    generate_report()