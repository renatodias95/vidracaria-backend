from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuração do banco de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos
class Perfil(Base):
    __tablename__ = "PerfisAluminio"
    codigo = Column(String, primary_key=True, index=True)
    descricao = Column(String)
    preco_barra = Column(String)
    peso_kg_por_metro = Column(String)
    unidade_medida = Column(String)
    fornecedor = Column(String)
    origem = Column(String, default='parceiro')

class Orcamento(Base):
    __tablename__ = "Orcamentos"
    id = Column(Integer, primary_key=True, index=True)
    numero_orcamento = Column(Integer)
    data_hora = Column(String)
    cliente_nome = Column(String)
    cliente_endereco = Column(String)
    cliente_contato = Column(String)
    itens = relationship("ItemOrcamento", back_populates="orcamento")

class ItemOrcamento(Base):
    __tablename__ = "ItensOrcamento"
    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer, ForeignKey('Orcamentos.id'))
    tipo_esquadria = Column(String)
    largura = Column(String)
    altura = Column(String)
    vidro_selecionado = Column(String)
    cor = Column(String)
    custo_perfis_item = Column(String)
    custo_vidro_item = Column(String)
    custo_acessorios_item = Column(String)
    custo_total_item = Column(String)
    valor_venda_item = Column(String)
    perfis_cortes_json = Column(String)
    acessorios_qtd_json = Column(String)
    detalhes_calculo_item = Column(String)
    orcamento = relationship("Orcamento", back_populates="itens")

class Acessorio(Base):
    __tablename__ = "Acessorios"
    codigo = Column(String, primary_key=True, index=True)
    descricao = Column(String)
    preco_unitario = Column(String)
    unidade_medida = Column(String)

class Vidro(Base):
    __tablename__ = "Vidros"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    preco_m2 = Column(String)
    unidade_medida = Column(String)

def criar_banco():
    print("Criando banco de dados e tabelas...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado com sucesso!")
    
    # Verificar se as tabelas foram criadas
    db = SessionLocal()
    try:
        print("\nTabelas criadas:")
        for table in Base.metadata.tables:
            print(f"- {table}")
    finally:
        db.close()

if __name__ == "__main__":
    criar_banco()
