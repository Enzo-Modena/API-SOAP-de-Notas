import pytest
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.exceptions import Fault

def get_client(wsdl_url, username=None, password=None):
    if username and password:
        wsse = UsernameToken(username, password)
        return Client(wsdl_url, wsse=wsse)
    return Client(wsdl_url)

def test_listar_alunos_vazio(soap_server):
    client = get_client(soap_server)
    alunos = client.service.listar_alunos()
    assert not alunos

def test_cadastrar_consultar_aluno(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    novo = client_adm.service.cadastrar_aluno(nome="João", nota1=8.0, nota2=7.0)
    assert novo.ra == 1
    assert novo.media == 7.4
    assert novo.situacao == "Aprovado"
    
    client_pub = get_client(soap_server)
    aluno = client_pub.service.consultar_aluno(ra=1)
    assert aluno.nome == "João"
    assert aluno.media == 7.4

def test_atualizar_notas(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    client_adm.service.cadastrar_aluno(nome="Maria", nota1=5.0, nota2=5.0)
    
    atualizado = client_adm.service.atualizar_notas(ra=1, nota1=10.0, nota2=10.0)
    assert atualizado.media == 10.0
    assert atualizado.situacao == "Aprovado"

def test_remover_aluno(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    client_adm.service.cadastrar_aluno(nome="Pedro", nota1=5.0, nota2=5.0)
    
    res = client_adm.service.remover_aluno(ra=1)
    assert "sucesso" in res.lower()
    
    with pytest.raises(Fault, match="Aluno não encontrado"):
        client_adm.service.consultar_aluno(ra=1)

def test_calcular_media_turma(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    client_adm.service.cadastrar_aluno(nome="A", nota1=10.0, nota2=10.0)
    client_adm.service.cadastrar_aluno(nome="B", nota1=5.0, nota2=5.0)
    
    client_pub = get_client(soap_server)
    media_turma = client_pub.service.calcular_media_turma()
    assert media_turma == 7.5

def test_autenticacao_invalida(soap_server):
    client_inv = get_client(soap_server, 'admin', 'senhaerrada')
    with pytest.raises(Fault, match="Credenciais inválidas"):
        client_inv.service.cadastrar_aluno(nome="X", nota1=1.0, nota2=1.0)

def test_rbac_usuario_sem_permissao(soap_server):
    client_user = get_client(soap_server, 'user', 'user123')
    with pytest.raises(Fault, match="Acesso negado"):
        client_user.service.cadastrar_aluno(nome="X", nota1=1.0, nota2=1.0)

def test_operacao_protegida_sem_credenciais(soap_server):
    client_pub = get_client(soap_server)
    with pytest.raises(Fault, match="Autenticação necessária"):
        client_pub.service.cadastrar_aluno(nome="X", nota1=1.0, nota2=1.0)

def test_cadastrar_aluno_validacoes(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')

    with pytest.raises(Fault, match="Nome do aluno é obrigatório"):
        client_adm.service.cadastrar_aluno(nome="   ", nota1=5.0, nota2=5.0)

    with pytest.raises(Fault, match="Nota 1"):
        client_adm.service.cadastrar_aluno(nome="Teste", nota1=15.0, nota2=5.0)

def test_atualizar_aluno_validacoes(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    client_adm.service.cadastrar_aluno(nome="Teste", nota1=5.0, nota2=5.0)

    with pytest.raises(Fault, match="Aluno não encontrado"):
        client_adm.service.atualizar_notas(ra=999, nota1=7.0, nota2=7.0)

    with pytest.raises(Fault, match="Nota 2"):
        client_adm.service.atualizar_notas(ra=1, nota1=7.0, nota2=-5.0)

def test_remover_aluno_inexistente(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')
    with pytest.raises(Fault, match="Aluno não encontrado"):
        client_adm.service.remover_aluno(ra=999)

def test_calcular_media_turma_vazia(soap_server):
    client_pub = get_client(soap_server)
    with pytest.raises(Fault, match="Nenhum aluno cadastrado"):
        client_pub.service.calcular_media_turma()
