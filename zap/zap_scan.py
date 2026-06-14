import urllib.request
import urllib.parse
import json
import time
import sys

ZAP_URL = "http://127.0.0.1:8090"
TARGET_URL = "http://web:5000"

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

def start_active_scan():
    print(f"Iniciando Active Scan no alvo: {TARGET_URL}...")
    api_url = f"{ZAP_URL}/JSON/ascan/action/scan/"
    params = urllib.parse.urlencode({"url": TARGET_URL, "recurse": "true"}).encode()
    
    res = rpc_call(api_url, data=params)
    scan_id = res.get("scan", res.get("scanId"))
    if not scan_id:
        print(f"Não foi possível obter o Scan ID. Resposta: {res}")
        sys.exit(1)
    return scan_id

def monitor_scan(scan_id):
    print(f"Scan ID {scan_id} iniciado. Monitorando progresso...")
    api_url = f"{ZAP_URL}/JSON/ascan/view/status/?scanId={scan_id}"
    
    for _ in range(60):
        res = rpc_call(api_url)
        progress = res.get("status", "0")
        print(f"Progresso: {progress}%")
        
        if progress == "100":
            print("Active Scan finalizado com sucesso!")
            return
        time.sleep(10)
        
    print("Erro: Timeout aguardando o Active Scan terminar.")
    sys.exit(1)

if __name__ == "__main__":
    scan_id = start_active_scan()
    monitor_scan(scan_id)