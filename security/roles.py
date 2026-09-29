from security.auth import USERS_DB

class Roles:
    ADM = "ADM"
    USER = "USER"

OPERATION_ROLES = {
    "cadastrar_aluno": [Roles.ADM],
    "atualizar_notas": [Roles.ADM],
    "remover_aluno": [Roles.ADM],
}

def verificar_acesso(username, operacao) -> bool:
    required_roles = OPERATION_ROLES.get(operacao)
    
    if not required_roles:
        return True
        
    if not username:
        return False
        
    user = USERS_DB.get(username)
    if not user:
        return False
        
    return user["role"] in required_roles
