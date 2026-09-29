import pytest
import threading
import time
from wsgiref.simple_server import make_server
import requests

from server import wsgi_app
from services.aluno_service import repo

class ServerThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.server = make_server('127.0.0.1', 0, wsgi_app)
        self.port = self.server.server_port

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()

@pytest.fixture(scope="session")
def soap_server():
    server_thread = ServerThread()
    server_thread.daemon = True
    server_thread.start()

    wsdl_url = f"http://127.0.0.1:{server_thread.port}/?wsdl"

    retries = 5
    while retries > 0:
        try:
            response = requests.get(wsdl_url)
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
            retries -= 1

    yield wsdl_url

    server_thread.shutdown()
    server_thread.join(timeout=2)

@pytest.fixture(autouse=True)
def cleanup_db():
    repo.reset()
    yield
