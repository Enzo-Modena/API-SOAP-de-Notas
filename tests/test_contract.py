import pytest
import xml.etree.ElementTree as ET
import requests

def get_wsdl_content(wsdl_url):
    response = requests.get(wsdl_url)
    assert response.status_code == 200
    return response.content

def test_wsdl_operacoes_presentes(soap_server):
    content = get_wsdl_content(soap_server)
    root = ET.fromstring(content)
    
    ns = {
        'wsdl': 'http://schemas.xmlsoap.org/wsdl/',
        'tns': 'academico.soap'
    }
    
    operacoes = [
        'consultar_aluno', 'listar_alunos', 'cadastrar_aluno',
        'atualizar_notas', 'remover_aluno', 'calcular_media_turma'
    ]
    
    port_types = root.findall('.//wsdl:portType/wsdl:operation', ns)
    op_names = [pt.get('name') for pt in port_types]
    
    for op in operacoes:
        assert op in op_names, f"Operação {op} não encontrada no WSDL"

def test_wsdl_tipo_aluno_model(soap_server):
    content = get_wsdl_content(soap_server)
    root = ET.fromstring(content)
    
    ns = {
        'xs': 'http://www.w3.org/2001/XMLSchema',
        'tns': 'academico.soap'
    }
    
    complex_types = root.findall('.//xs:complexType', ns)
    aluno_model_type = None
    for ct in complex_types:
        if ct.get('name') == 'AlunoModel':
            aluno_model_type = ct
            break
            
    assert aluno_model_type is not None, "Tipo AlunoModel não encontrado no WSDL"
    
    elements = aluno_model_type.findall('.//xs:element', ns)
    element_names = [el.get('name') for el in elements]
    
    expected_fields = ['media', 'nome', 'nota1', 'nota2', 'ra', 'situacao']
    for field in expected_fields:
        assert field in element_names, f"Campo {field} não encontrado em AlunoModel"
