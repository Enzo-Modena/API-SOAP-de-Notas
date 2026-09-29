from wsgiref.simple_server import make_server
from server import wsgi_app

def run_server():
    print("=" * 50)
    print("Servidor SOAP rodando na porta 8000...")
    print("WSDL disponível em: http://127.0.0.1:8000/?wsdl")
    print("=" * 50)
    print("Pressione Ctrl+C para encerrar.")
    
    server = make_server('127.0.0.1', 8000, wsgi_app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    run_server()