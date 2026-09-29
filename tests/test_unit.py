import pytest
import xml.etree.ElementTree as ET
from services.business_logic import calcular_media, determinar_situacao, validar_notas
from security.auth import autenticar, extrair_credenciais_wsse
from security.roles import verificar_acesso
from security.rate_limit import check_rate_limit

def test_calcular_media():
    assert calcular_media(8.0, 7.0) == pytest.approx(7.4)
    assert calcular_media(10.0, 10.0) == pytest.approx(10.0)
    assert calcular_media(0.0, 0.0) == pytest.approx(0.0)

def test_determinar_situacao():
    assert determinar_situacao(7.0) == "Aprovado"
    assert determinar_situacao(7.1) == "Aprovado"
    assert determinar_situacao(5.0) == "Recuperação"
    assert determinar_situacao(6.9) == "Recuperação"
    assert determinar_situacao(4.9) == "Reprovado"
    assert determinar_situacao(0.0) == "Reprovado"

def test_validar_notas_validas():
    validar_notas(0.0, 10.0)
    validar_notas(5.5, 7.3)
    validar_notas(10.0, 0.0)

def test_validar_notas_invalidas():
    with pytest.raises(ValueError, match="Nota 1"):
        validar_notas(-1.0, 10.0)
    with pytest.raises(ValueError, match="Nota 1"):
        validar_notas(10.1, 10.0)
    with pytest.raises(ValueError, match="Nota 2"):
        validar_notas(10.0, -0.1)
    with pytest.raises(ValueError, match="Nota 2"):
        validar_notas(10.0, 11.0)

def test_auth_edge_cases():
    assert autenticar("usuario_fantasma", "senha123") is False

    class DummyCtx:
        in_document = None
    assert extrair_credenciais_wsse(DummyCtx()) == (None, None)

    class DummyCtxNoHeader:
        in_document = ET.fromstring("<Envelope xmlns='http://schemas.xmlsoap.org/soap/envelope/'><Body/></Envelope>")
    assert extrair_credenciais_wsse(DummyCtxNoHeader()) == (None, None)

    class DummyCtxNoSec:
        in_document = ET.fromstring("<Envelope xmlns='http://schemas.xmlsoap.org/soap/envelope/'><Header/><Body/></Envelope>")
    assert extrair_credenciais_wsse(DummyCtxNoSec()) == (None, None)

    class DummyCtxNoToken:
        in_document = ET.fromstring(
            "<Envelope xmlns='http://schemas.xmlsoap.org/soap/envelope/'>"
            "<Header><wsse:Security xmlns:wsse='http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd'/></Header>"
            "<Body/></Envelope>"
        )
    assert extrair_credenciais_wsse(DummyCtxNoToken()) == (None, None)
    assert extrair_credenciais_wsse("nao_e_contexto") == (None, None)

def test_roles_edge_cases():
    assert verificar_acesso("admin", "operacao_livre") is True
    assert verificar_acesso(None, "operacao_livre") is True
    assert verificar_acesso(None, "cadastrar_aluno") is False
    assert verificar_acesso("fantasma", "cadastrar_aluno") is False

def test_rate_limit_edge_cases():
    assert check_rate_limit(None) is True
    assert check_rate_limit("") is True
