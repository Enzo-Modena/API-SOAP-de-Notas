"""
Compatibilidade Spyne + Python 3.13

O Spyne internamente depende do pacote 'six' que referencia módulos
movidos/removidos a partir do Python 3.10+. Este módulo registra os
mapeamentos necessários em sys.modules ANTES de qualquer import do Spyne.

Deve ser importado como primeira linha em qualquer ponto de entrada
(server.py, conftest.py, etc).
"""

import sys
import collections.abc
import http.cookies
import urllib.parse
import urllib.request

sys.modules['spyne.util.six.moves.collections_abc'] = collections.abc
sys.modules['spyne.util.six.moves.http_cookies'] = http.cookies
sys.modules['spyne.util.six.moves.urllib'] = urllib
sys.modules['spyne.util.six.moves.urllib.parse'] = urllib.parse
sys.modules['spyne.util.six.moves.urllib.request'] = urllib.request
