import urllib.request
import urllib.parse
import urllib.error
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
    except urllib.error.HTTPError as e:
        # Captura o erro 400 e lê o JSON de resposta real do ZAP
        print(f"Erro HTTP {e.code}: {e.reason}")
        try:
            error_body = e.read().decode()
            print(f"Detalhes do erro do ZAP: {error_body}")
        except Exception:
            print("Não foi possível ler os detalhes do erro do ZAP.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro na chamada da API ({url}): {e}")
        sys.exit(1)

def generate_report():
    print("Solicitando geração do relatório HTML ao ZAP...")
    api_url = f"{ZAP_URL}/JSON/reports/action/generate/"
    
    # O ZAP exige a presença de toda a estrutura de parâmetros da API.
    # Deixamos os filtros opcionais vazios ("") para ele processar tudo.
    params = urllib.parse.urlencode({
        "title": "DAST Scan Report",
        "template": "html-report",
        "theme": "",
        "description": "",
        "contexts": "",
        "sites": "",
        "sections": "",
        "includedLevels": "",
        "reportDir": "/zap/wrk",
        "reportFile": "zap-report.html"
    }).encode()
    
    res = rpc_call(api_url, data=params)
    print(f"Relatório gerado com sucesso: {res}")

if __name__ == "__main__":
    generate_report()