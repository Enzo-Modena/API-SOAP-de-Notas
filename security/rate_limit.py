import time

historico_ips = {}
LIMITE_POR_MINUTO = 100

def check_rate_limit(ip_address: str) -> bool:
    if not ip_address:
        return True

    agora = time.time()
    dados = historico_ips.get(ip_address)

    if not dados or (agora - dados["tempo_inicio"] > 60):
        historico_ips[ip_address] = {"contador": 1, "tempo_inicio": agora}
        return True

    if dados["contador"] < LIMITE_POR_MINUTO:
        dados["contador"] += 1
        return True

    return False

def reset_rate_limit():
    historico_ips.clear()
