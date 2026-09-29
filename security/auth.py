import hashlib

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

USERS_DB = {
    "admin": {
        "password_hash": _hash_password("admin123"),
        "role": "ADM"
    },
    "user": {
        "password_hash": _hash_password("user123"),
        "role": "USER"
    }
}

def autenticar(username: str, password: str) -> bool:
    user = USERS_DB.get(username)
    if not user:
        return False
    return _hash_password(password) == user["password_hash"]

def extrair_credenciais_wsse(ctx):
    try:
        if ctx.in_document is None:
            return None, None
            
        header = ctx.in_document.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Header')
        if header is None:
            return None, None
            
        security = header.find('.//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Security')
        if security is None:
            return None, None
            
        username_token = security.find('.//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}UsernameToken')
        if username_token is None:
            return None, None
            
        username_el = username_token.find('.//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Username')
        password_el = username_token.find('.//{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Password')
        
        if username_el is not None and password_el is not None:
            return username_el.text, password_el.text
            
    except AttributeError:
        pass
        
    return None, None
