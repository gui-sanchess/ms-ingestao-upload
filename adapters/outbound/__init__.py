import os
import httpx
from domain.ports import IaClientPort

class HttpIaClientAdapter(IaClientPort):
    def __init__(self):
        # Agora ele pega do sistema operacional, ou usa um valor padrão para testes locais
        self.url_ia = os.getenv("IA_SERVICE_URL", "http://localhost:5004/api/analisar")