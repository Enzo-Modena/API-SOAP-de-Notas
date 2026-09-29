import compat  # noqa: F401
from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.fault import Fault

from services.aluno_service import AlunoService, repo
from security.auth import autenticar, extrair_credenciais_wsse
from security.roles import verificar_acesso, OPERATION_ROLES
from security.rate_limit import check_rate_limit

dados_iniciais = [
    {"nome": "Enzo", "nota1": 8.0, "nota2": 7.0},
    {"nome": "Pedro", "nota1": 9.0, "nota2": 6.0},
    {"nome": "Julia", "nota1": 10.0, "nota2": 9.0},
]

for dados in dados_iniciais:
    repo.inserir(dados["nome"], dados["nota1"], dados["nota2"])

def _on_method_call(ctx):
    ip_address = None
    if ctx.transport and hasattr(ctx.transport, 'req'):
        ip_address = ctx.transport.req.get('REMOTE_ADDR')

    if ip_address and not check_rate_limit(ip_address):
        raise Fault("Client", "Rate limit excedido. Tente novamente mais tarde.")

    method_name = ctx.descriptor.name

    if method_name in OPERATION_ROLES:
        username, password = extrair_credenciais_wsse(ctx)

        if not username or not password:
            raise Fault("Client", "Autenticação necessária")

        if not autenticar(username, password):
            raise Fault("Client", "Credenciais inválidas")

        if not verificar_acesso(username, method_name):
            raise Fault("Client", "Acesso negado: permissão insuficiente")

AlunoService.event_manager.add_listener('method_call', _on_method_call)

application = Application(
    [AlunoService],
    tns='academico.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)