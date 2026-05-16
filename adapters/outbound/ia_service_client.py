import httpx
from domain.ports import IaClientPort

class HttpIaClientAdapter(IaClientPort):
    def __init__(self):
        # A URL do seu outro microsserviço
        self.url_ia = "http://ms-processamento-ia:5004/api/analisar"

    async def classificar_documento(self, texto: str) -> dict:
        # Timeout de 30 segundos porque a IA do Google leva um tempinho para ler
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.url_ia, json={"texto": texto})
                response.raise_for_status() # Verifica se não deu erro 400 ou 500
                dados = response.json()
                return dados.get("dados_extraidos", {})
            except Exception as e:
                print(f"Erro ao comunicar com ms-ia: {e}")
                # Retorna dados padrão em caso de falha para não quebrar o upload
                return {
                    "tipo_classificado": "Falha na IA",
                    "tags": ["erro_comunicacao"],
                    "resumo": "Não foi possível conectar ao serviço de IA."
                }