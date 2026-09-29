import sys
import zeep
from zeep.wsse.username import UsernameToken
from zeep.exceptions import Fault

def print_separator(title):
    print(f"\n{'='*50}")
    print(f"--- {title} ---")
    print(f"{'='*50}\n")

def run_client():
    wsdl_url = 'http://127.0.0.1:8000/?wsdl'
    print(f"Conectando ao servidor SOAP em: {wsdl_url}...")
    
    try:
        client_pub = zeep.Client(wsdl=wsdl_url)
        
        wsse = UsernameToken('admin', 'admin123')
        client_adm = zeep.Client(wsdl=wsdl_url, wsse=wsse)
        
        wsse_user = UsernameToken('user', 'user123')
        client_user = zeep.Client(wsdl=wsdl_url, wsse=wsse_user)
    except Exception as e:
        print(f"Erro ao conectar ao servidor na porta 8000: {e}")
        sys.exit(1)

    print_separator("1. Listando Alunos Iniciais (Público)")
    alunos = client_pub.service.listar_alunos()
    for aluno in alunos:
        print(f"RA: {aluno.ra} | Nome: {aluno.nome} | Média: {aluno.media} | Situação: {aluno.situacao}")

    print_separator("2. Cadastrando Novo Aluno (ADM)")
    try:
        novo = client_adm.service.cadastrar_aluno(nome="Carlos Souza", nota1=5.0, nota2=4.0)
        print(f"Sucesso! Aluno cadastrado: RA {novo.ra}, Nome: {novo.nome}, Situação: {novo.situacao}")
    except Fault as e:
        print(f"Falha: {e}")

    print_separator("3. Tentando Cadastrar Aluno sem Permissão (USER)")
    try:
        client_user.service.cadastrar_aluno(nome="Invasor", nota1=10.0, nota2=10.0)
    except Fault as e:
        print(f"Erro esperado capturado: {e.message}")
        
    print_separator("4. Tentando Cadastrar Aluno sem Autenticação (Público)")
    try:
        client_pub.service.cadastrar_aluno(nome="Fantasma", nota1=10.0, nota2=10.0)
    except Fault as e:
        print(f"Erro esperado capturado: {e.message}")

    print_separator("5. Consultando Aluno Específico (Público)")
    try:
        aluno = client_pub.service.consultar_aluno(ra=4)
        print(f"RA: {aluno.ra} | Nome: {aluno.nome} | Média: {aluno.media} | Situação: {aluno.situacao}")
    except Fault as e:
        print(f"Falha: {e}")

    print_separator("6. Atualizando Notas do Aluno (ADM)")
    try:
        atualizado = client_adm.service.atualizar_notas(ra=4, nota1=8.0, nota2=7.0)
        print(f"Sucesso! Notas atualizadas. Nova média: {atualizado.media}, Nova situação: {atualizado.situacao}")
    except Fault as e:
        print(f"Falha: {e}")

    print_separator("7. Calculando Média da Turma (Público)")
    try:
        media_turma = client_pub.service.calcular_media_turma()
        print(f"Média geral da turma: {media_turma:.2f}")
    except Fault as e:
        print(f"Falha: {e}")

    print_separator("8. Removendo Aluno (ADM)")
    try:
        msg = client_adm.service.remover_aluno(ra=4)
        print(f"Mensagem do servidor: {msg}")
    except Fault as e:
        print(f"Falha: {e}")
        
    print_separator("Estado Final da Turma")
    alunos_final = client_pub.service.listar_alunos()
    for aluno in alunos_final:
        print(f"RA: {aluno.ra} | Nome: {aluno.nome} | Situação: {aluno.situacao}")

if __name__ == '__main__':
    run_client()
