from domain.entities import Artefato
from domain.ports import FileExtractorPort, ArtefatoRepositoryPort, IaClientPort

class ProcessarUploadUseCase:
    def __init__(self, extractor: FileExtractorPort, repository: ArtefatoRepositoryPort, ia_client: IaClientPort):
        self.extractor = extractor
        self.repository = repository
        self.ia_client = ia_client

    async def executar(self, conteudo_bytes: bytes, nome_arquivo: str, projeto_id: int) -> Artefato:
        texto = self.extractor.extrair_texto(conteudo_bytes, nome_arquivo)
        resultado_ia = await self.ia_client.classificar_documento(texto)

        # MÁGICA AQUI: Pega as tags da IA e força a adição da tag "Upload"
        tags_finais = resultado_ia.get("tags", [])
        if "Upload" not in tags_finais:
            tags_finais.append("Upload")

        novo_artefato = Artefato(
            nome_arquivo=nome_arquivo,
            conteudo_extraido=texto,
            projeto_id=projeto_id,
            tipo_classificado=resultado_ia.get("tipo_classificado", "Desconhecido"),
            tags=tags_finais, # <-- Passa a lista atualizada
            resumo=resultado_ia.get("resumo", "Sem resumo.")
        )

        return self.repository.salvar(novo_artefato)