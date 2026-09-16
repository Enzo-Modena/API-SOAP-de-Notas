from spyne import Application, rpc, ServiceBase, Unicode, Integer, Float, ComplexModel  
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class AlunoModel(ComplexModel):
    nome = Unicode
    nota1 = Float
    nota2 = Float
    media = Float
    situacao = Unicode

alunos = {
    1: {"nome": "Enzo", "nota1": 8.0, "nota2": 7.0, "media": "7.75"},
    2: {"nome": "Pedro", "nota1": 9.0, "nota2": 6.0, "media": "7.5"},
    3: {"nome": "Julia", "nota1": 10.0, "nota2": 9.0, "media": "9.5"}
}

class AlunoService(ServiceBase):
    @rpc(Integer, _returns=AlunoModel)
    def consultar_aluno(ctx,ra):
        """Consulta a situação acadêmica de um aluno pelo RA."""
        dados = alunos.get(ra)

        if not dados:
            return AlunoModel(situacao="Aluno não encontrado")
        
        media = (dados["nota1"] + dados["nota2"])/2
        if media>= 7.0:
            situacao = "Aprovado"
        elif media>= 5.0:
            situacao = "Recuperação"
        else:
            situacao = "Reprovado"

        return AlunoModel(
            nome=dados["nome"],
            nota1=dados["nota1"],
            nota2=dados["nota2"],
            media=media,
            situacao=situacao
        )

application = Application(
    [AlunoService],
    tns='academico.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    print("servidor soap rodando na porta 8000...")
    print("WSDL disponível em: http://127.0.0.1:8000/?wsdl")
    server = make_server('127.0.0.1',8000,wsgi_app)
    server.serve_forever()