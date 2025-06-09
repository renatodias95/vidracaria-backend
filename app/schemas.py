from pydantic import BaseModel

class AcessorioBase(BaseModel):
    codigo: str
    descricao: str
    preco_unitario: str
    unidade_medida: str
    class Config:
        orm_mode = True

class VidroBase(BaseModel):
    id: int
    descricao: str
    preco_m2: str
    unidade_medida: str
    class Config:
        orm_mode = True

from pydantic import BaseModel

class PerfilBase(BaseModel):
    codigo: str
    descricao: str
    preco_barra: str
    peso_kg_por_metro: str
    unidade_medida: str
    fornecedor: str
    origem: str = 'parceiro'  # 'parceiro' ou 'usuario'

class Perfil(PerfilBase):
    class Config:
        orm_mode = True

class ItemOrcamentoBase(BaseModel):
    id: int
    orcamento_id: int
    tipo_esquadria: str
    largura: str
    altura: str
    vidro_selecionado: str | None = None
    cor: str
    custo_perfis_item: str
    custo_vidro_item: str
    custo_acessorios_item: str
    custo_total_item: str
    valor_venda_item: str
    perfis_cortes_json: str | None = None
    acessorios_qtd_json: str | None = None
    detalhes_calculo_item: str | None = None

    class Config:
        orm_mode = True

class OrcamentoBase(BaseModel):
    id: int
    numero_orcamento: int
    data_hora: str
    cliente_nome: str | None = None
    cliente_endereco: str | None = None
    cliente_contato: str | None = None
    valor_total_custo: str
    valor_total_venda: str
    aprovado: int
    detalhes_otimizacao: str | None = None
    gastos_extras: str | None = None
    plano_corte_json: str | None = None
    usuario_criacao: str

    class Config:
        orm_mode = True

class OrcamentoComItens(OrcamentoBase):
    itens: list[ItemOrcamentoBase] = []

# --- Estoque Schemas ---
class EstoqueBase(BaseModel):
    nome_item: str
    tipo_item: str
    quantidade: int = 0
    unidade: str = 'un'
    localizacao: str = ''
    observacao: str = ''
    data_atualizacao: str = ''

class EstoqueCreate(EstoqueBase):
    pass

class Estoque(EstoqueBase):
    id: int
    class Config:
        from_attributes = True

# --- Projeto Schemas ---
class ProjetoBase(BaseModel):
    nome: str
    tipo: str
    descricao: str = ''
    data_criacao: str = ''

class ProjetoCreate(ProjetoBase):
    pass

class Projeto(ProjetoBase):
    id: int
    class Config:
        from_attributes = True

# --- Autenticação ---
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UsuarioBase(BaseModel):
    username: str
    email: EmailStr
    nome: str
    admin: bool = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nome: Optional[str] = None
    password: Optional[str] = None
    ativo: Optional[bool] = None

class Usuario(UsuarioBase):
    id: int
    ativo: bool
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        orm_mode = True

class LoginData(BaseModel):
    username: str
    password: str
