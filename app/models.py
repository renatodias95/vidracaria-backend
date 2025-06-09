from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class Perfil(Base):
    __tablename__ = "PerfisAluminio"
    codigo = Column(String, primary_key=True, index=True)
    descricao = Column(String)
    preco_barra = Column(String)
    peso_kg_por_metro = Column(String)
    unidade_medida = Column(String)
    fornecedor = Column(String)
    # Coluna origem é opcional com valor padrão 'parceiro'
    origem = Column(String, default='parceiro', nullable=True)  # 'parceiro' ou 'usuario'

class Orcamento(Base):
    __tablename__ = "Orcamentos"
    id = Column(Integer, primary_key=True, index=True)
    numero_orcamento = Column(Integer)
    data_hora = Column(String)
    cliente_nome = Column(String)
    cliente_endereco = Column(String)
    cliente_contato = Column(String)
    valor_total_custo = Column(String)
    valor_total_venda = Column(String)
    aprovado = Column(Integer)
    detalhes_otimizacao = Column(String)
    gastos_extras = Column(String)
    plano_corte_json = Column(String)
    usuario_criacao = Column(String)

class ItemOrcamento(Base):
    __tablename__ = "ItensOrcamento"
    id = Column(Integer, primary_key=True, index=True)
    orcamento_id = Column(Integer)
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

class Acessorio(Base):
    __tablename__ = "Acessorios"
    codigo = Column(String, primary_key=True, index=True)
    descricao = Column(String)
    preco_unitario = Column(String)
    unidade_medida = Column(String)

class Estoque(Base):
    __tablename__ = "Estoque"
    id = Column(Integer, primary_key=True, index=True)
    nome_item = Column(String, nullable=False)
    tipo_item = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    unidade = Column(String, nullable=False, default='un')
    localizacao = Column(String, default='')
    observacao = Column(String, default='')
    data_atualizacao = Column(String, default='')

class Projeto(Base):
    __tablename__ = "Projetos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # esquadria, vidro temperado, etc
    descricao = Column(String)
    data_criacao = Column(String)

class Vidro(Base):
    __tablename__ = "Vidros"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    preco_m2 = Column(String)
    unidade_medida = Column(String)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
