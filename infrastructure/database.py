import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Captura as credenciais do banco
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_SCHEMA = os.getenv("DB_SCHEMA", "upload")

# Monta a String de Conexão padrão do PostgreSQL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# O pulo do gato: Cria o motor do banco já apontando para o schema correto ('upload')
# O connect_args com 'options' força o PostgreSQL a usar o nosso schema.
engine = create_engine(
    DATABASE_URL,
    connect_args={"options": f"-csearch_path={DB_SCHEMA}"},
    echo=True # Útil no desenvolvimento para ver os comandos SQL no terminal
)

# Fábrica de Sessões: É o que o FastAPI vai usar para abrir e fechar conexões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base que nossas tabelas vão herdar
Base = declarative_base()

# Dependência do FastAPI para injetar o banco de dados nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()