from spyne import ServiceBase, rpc, Integer, Unicode, Float, Array
from spyne.model.fault import Fault
from models.aluno import AlunoModel
from services.business_logic import calcular_media, determinar_situacao, validar_notas

class AlunoRepository:
    def __init__(self):
        self._alunos_db: dict[int, dict] = {}
        self._proximo_ra: int = 1

    def inserir(self, nome: str, nota1: float, nota2: float) -> dict:
        media = calcular_media(nota1, nota2)
        situacao = determinar_situacao(media)
        ra = self._proximo_ra
        self._proximo_ra += 1

        aluno = {
            "ra": ra,
            "nome": nome.strip(),
            "nota1": nota1,
            "nota2": nota2,
            "media": media,
            "situacao": situacao,
        }
        self._alunos_db[ra] = aluno
        return aluno

    def buscar(self, ra: int) -> dict | None:
        return self._alunos_db.get(ra)

    def listar(self) -> list[dict]:
        return list(self._alunos_db.values())

    def atualizar(self, ra: int, nota1: float, nota2: float) -> dict | None:
        aluno = self._alunos_db.get(ra)
        if aluno is None:
            return None
        media = calcular_media(nota1, nota2)
        situacao = determinar_situacao(media)
        aluno["nota1"] = nota1
        aluno["nota2"] = nota2
        aluno["media"] = media
        aluno["situacao"] = situacao
        return aluno

    def remover(self, ra: int) -> bool:
        if ra in self._alunos_db:
            del self._alunos_db[ra]
            return True
        return False

    def reset(self):
        self._alunos_db.clear()
        self._proximo_ra = 1

repo = AlunoRepository()

class AlunoService(ServiceBase):
    @rpc(Integer(min_occurs=1), _returns=AlunoModel)
    def consultar_aluno(ctx, ra):
        aluno_data = repo.buscar(ra)
        if not aluno_data:
            raise Fault("Client", "Aluno não encontrado")
        return AlunoModel(**aluno_data)

    @rpc(_returns=Array(AlunoModel))
    def listar_alunos(ctx):
        return [AlunoModel(**data) for data in repo.listar()]

    @rpc(Unicode(min_occurs=1), Float(min_occurs=1), Float(min_occurs=1), _returns=AlunoModel)
    def cadastrar_aluno(ctx, nome, nota1, nota2):
        if not nome or not nome.strip():
            raise Fault("Client", "Nome do aluno é obrigatório")
        try:
            validar_notas(nota1, nota2)
        except ValueError as e:
            raise Fault("Client", str(e))

        aluno_data = repo.inserir(nome, nota1, nota2)
        return AlunoModel(**aluno_data)

    @rpc(Integer(min_occurs=1), Float(min_occurs=1), Float(min_occurs=1), _returns=AlunoModel)
    def atualizar_notas(ctx, ra, nota1, nota2):
        try:
            validar_notas(nota1, nota2)
        except ValueError as e:
            raise Fault("Client", str(e))

        aluno_data = repo.atualizar(ra, nota1, nota2)
        if aluno_data is None:
            raise Fault("Client", "Aluno não encontrado")
        return AlunoModel(**aluno_data)

    @rpc(Integer(min_occurs=1), _returns=Unicode)
    def remover_aluno(ctx, ra):
        if not repo.remover(ra):
            raise Fault("Client", "Aluno não encontrado")
        return "Aluno removido com sucesso"

    @rpc(_returns=Float)
    def calcular_media_turma(ctx):
        alunos = repo.listar()
        if not alunos:
            raise Fault("Client", "Nenhum aluno cadastrado")
        soma_medias = sum(a["media"] for a in alunos)
        return round(soma_medias / len(alunos), 2)
