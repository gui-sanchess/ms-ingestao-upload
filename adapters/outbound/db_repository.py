from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY
from sqlalchemy.orm import Session
from domain.entities import Artefato
from domain.ports import ArtefatoRepositoryPort
from infrastructure.database import Base


class ArtefatoModel(Base):
    __tablename__ = "artefatos_brutos"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, nullable=False, index=True)
    nome_arquivo = Column(String, nullable=False)
    conteudo_extraido = Column(Text, nullable=False)
    tipo_classificado = Column(String, nullable=True)
    tags = Column(ARRAY(String), default=[])
    resumo = Column(Text, nullable=True)
    data_upload = Column(DateTime, nullable=False)


class PostgresArtefatoRepository(ArtefatoRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, artefato: Artefato) -> Artefato:
        novo_artefato = ArtefatoModel(
            projeto_id=artefato.projeto_id,
            nome_arquivo=artefato.nome_arquivo,
            conteudo_extraido=artefato.conteudo_extraido,
            tipo_classificado=artefato.tipo_classificado,
            tags=artefato.tags,
            resumo=artefato.resumo,
            data_upload=artefato.data_upload
        )
        self.db.add(novo_artefato)
        self.db.commit()
        self.db.refresh(novo_artefato)
        artefato.id = novo_artefato.id
        return artefato

    def buscar_por_projeto(self, projeto_id: int) -> list[Artefato]:
        # Faz o SELECT filtrando pelo ID do projeto
        modelos = self.db.query(ArtefatoModel).filter(ArtefatoModel.projeto_id == projeto_id).all()

        # Mapeia o resultado do banco (Model) de volta para o objeto de negócio (Entidade)
        artefatos = []
        for m in modelos:
            artefatos.append(Artefato(
                id=m.id,
                nome_arquivo=m.nome_arquivo,
                conteudo_extraido=m.conteudo_extraido,
                projeto_id=m.projeto_id,
                tipo_classificado=m.tipo_classificado,
                tags=m.tags,
                resumo=m.resumo,
                data_upload=m.data_upload
            ))
        return artefatos

    def deletar(self, id: int) -> bool:
        artefato = self.db.query(ArtefatoModel).filter(ArtefatoModel.id == id).first()
        if artefato:
            self.db.delete(artefato)
            self.db.commit()
            return True
        return False