import pytest
from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.exceptions import Fault
from security.rate_limit import check_rate_limit, reset_rate_limit, LIMITE_POR_MINUTO

def get_client(wsdl_url, username=None, password=None):
    if username and password:
        wsse = UsernameToken(username, password)
        return Client(wsdl_url, wsse=wsse)
    return Client(wsdl_url)

def test_fluxo_academico_completo(soap_server):
    client_adm = get_client(soap_server, 'admin', 'admin123')

    a1 = client_adm.service.cadastrar_aluno(nome="João", nota1=8.0, nota2=7.0)
    a2 = client_adm.service.cadastrar_aluno(nome="Maria", nota1=5.0, nota2=4.0)

    assert a1.situacao == "Aprovado"
    assert a2.situacao == "Reprovado"

    client_pub = get_client(soap_server)
    alunos = client_pub.service.listar_alunos()
    assert len(alunos) == 2

    media = client_pub.service.calcular_media_turma()
    assert media == pytest.approx(5.9)

    client_user = get_client(soap_server, 'user', 'user123')
    with pytest.raises(Fault, match="Acesso negado"):
        client_user.service.remover_aluno(ra=1)

    client_adm.service.remover_aluno(ra=1)
    alunos = client_pub.service.listar_alunos()
    assert len(alunos) == 1
    assert alunos[0].nome == "Maria"

def test_rate_limit():
    reset_rate_limit()
    ip = "192.168.1.100"
    for _ in range(LIMITE_POR_MINUTO):
        assert check_rate_limit(ip) is True
    assert check_rate_limit(ip) is False
