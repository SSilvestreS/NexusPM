"""
Schemas para busca full-text
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    """Schema para busca avançada"""
    terms: Optional[List[str]] = Field(None, description="Termos de busca")
    exact_phrase: Optional[str] = Field(None, description="Frase exata")
    tags: Optional[List[str]] = Field(None, description="Tags para filtrar")
    entity_type: Optional[str] = Field(None, description="Tipo de entidade (project, task, comment, all)")
    project_id: Optional[int] = Field(None, description="ID do projeto para filtrar")
    author_id: Optional[int] = Field(None, description="ID do autor para filtrar")
    date_from: Optional[str] = Field(None, description="Data de início (YYYY-MM-DD)")
    date_to: Optional[str] = Field(None, description="Data de fim (YYYY-MM-DD)")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")


class SearchResult(BaseModel):
    """Schema para resultado de busca"""
    id: int = Field(..., description="ID da entidade")
    entity_type: str = Field(..., description="Tipo de entidade (project, task, comment)")
    title: str = Field(..., description="Título ou nome da entidade")
    content: str = Field(..., description="Conteúdo ou descrição da entidade")
    author: str = Field(..., description="Nome do autor")
    author_id: int = Field(..., description="ID do autor")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")
    project_id: Optional[int] = Field(None, description="ID do projeto")
    task_id: Optional[int] = Field(None, description="ID da tarefa")
    comment_id: Optional[int] = Field(None, description="ID do comentário")
    relevance_score: float = Field(..., description="Pontuação de relevância")
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Schema para resposta de busca"""
    items: List[SearchResult] = Field(..., description="Resultados da busca")
    total: int = Field(..., description="Total de resultados")
    page: int = Field(..., description="Página atual")
    size: int = Field(..., description="Tamanho da página")
    pages: int = Field(..., description="Total de páginas")
    query: str = Field(..., description="Termo de busca utilizado")
    entity_type: str = Field(..., description="Tipo de entidade filtrada")
    
    class Config:
        from_attributes = True


class SearchSuggestion(BaseModel):
    """Schema para sugestão de busca"""
    term: str = Field(..., description="Termo sugerido")
    type: str = Field(..., description="Tipo da sugestão (project, task, tag)")
    count: int = Field(..., description="Número de ocorrências")
    
    class Config:
        from_attributes = True


class SearchFilters(BaseModel):
    """Schema para filtros de busca"""
    entity_types: List[str] = Field(default=["project", "task", "comment"], description="Tipos de entidade")
    date_range: Optional[str] = Field(None, description="Intervalo de datas (today, week, month, year)")
    authors: List[int] = Field(default=[], description="IDs dos autores para filtrar")
    projects: List[int] = Field(default=[], description="IDs dos projetos para filtrar")
    tags: List[str] = Field(default=[], description="Tags para filtrar")
    status: Optional[str] = Field(None, description="Status para filtrar")
    
    class Config:
        from_attributes = True


class SearchStatistics(BaseModel):
    """Schema para estatísticas de busca"""
    total_results: int = Field(..., description="Total de resultados")
    results_by_type: dict = Field(..., description="Resultados por tipo de entidade")
    top_authors: List[dict] = Field(..., description="Principais autores")
    top_tags: List[dict] = Field(..., description="Principais tags")
    search_time_ms: float = Field(..., description="Tempo de busca em milissegundos")
    
    class Config:
        from_attributes = True
