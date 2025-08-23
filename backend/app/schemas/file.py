"""
Schemas para gerenciamento de arquivos
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    """Schema para metadados de arquivo"""
    filename: str = Field(..., description="Nome original do arquivo")
    file_size: int = Field(..., description="Tamanho do arquivo em bytes")
    file_type: str = Field(..., description="Tipo de arquivo (image, document, etc.)")
    mime_type: str = Field(..., description="Tipo MIME do arquivo")
    description: Optional[str] = Field(None, description="Descrição do arquivo")
    tags: List[str] = Field(default=[], description="Tags do arquivo")


class FileUploadResponse(BaseModel):
    """Schema para resposta de upload de arquivo"""
    id: int = Field(..., description="ID do arquivo")
    filename: str = Field(..., description="Nome original do arquivo")
    file_size: int = Field(..., description="Tamanho do arquivo em bytes")
    file_type: str = Field(..., description="Tipo de arquivo")
    mime_type: str = Field(..., description="Tipo MIME do arquivo")
    project_id: Optional[int] = Field(None, description="ID do projeto")
    task_id: Optional[int] = Field(None, description="ID da tarefa")
    uploaded_by: int = Field(..., description="ID do usuário que fez upload")
    upload_date: datetime = Field(..., description="Data do upload")
    
    class Config:
        from_attributes = True


class FileUpdateRequest(BaseModel):
    """Schema para atualização de arquivo"""
    description: Optional[str] = Field(None, description="Nova descrição do arquivo")
    tags: Optional[List[str]] = Field(None, description="Novas tags do arquivo")


class FileDetailResponse(BaseModel):
    """Schema para detalhes completos de arquivo"""
    id: int = Field(..., description="ID do arquivo")
    filename: str = Field(..., description="Nome original do arquivo")
    stored_filename: str = Field(..., description="Nome do arquivo no servidor")
    file_path: str = Field(..., description="Caminho do arquivo no servidor")
    file_size: int = Field(..., description="Tamanho do arquivo em bytes")
    file_type: str = Field(..., description="Tipo de arquivo")
    mime_type: str = Field(..., description="Tipo MIME do arquivo")
    description: Optional[str] = Field(None, description="Descrição do arquivo")
    tags: List[str] = Field(default=[], description="Tags do arquivo")
    project_id: Optional[int] = Field(None, description="ID do projeto")
    task_id: Optional[int] = Field(None, description="ID da tarefa")
    uploaded_by: int = Field(..., description="ID do usuário que fez upload")
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: Optional[datetime] = Field(None, description="Data de atualização")
    
    # Relacionamentos
    uploaded_by_user: Optional[dict] = Field(None, description="Usuário que fez upload")
    project: Optional[dict] = Field(None, description="Projeto relacionado")
    task: Optional[dict] = Field(None, description="Tarefa relacionada")
    
    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    """Schema para lista de arquivos"""
    items: List[FileDetailResponse] = Field(..., description="Lista de arquivos")
    total: int = Field(..., description="Total de arquivos")
    page: int = Field(..., description="Página atual")
    size: int = Field(..., description="Tamanho da página")
    pages: int = Field(..., description="Total de páginas")
    
    class Config:
        from_attributes = True


class FileSearchQuery(BaseModel):
    """Schema para busca de arquivos"""
    filename: Optional[str] = Field(None, description="Nome do arquivo para buscar")
    file_type: Optional[str] = Field(None, description="Tipo de arquivo para filtrar")
    project_id: Optional[int] = Field(None, description="ID do projeto para filtrar")
    task_id: Optional[int] = Field(None, description="ID da tarefa para filtrar")
    uploaded_by: Optional[int] = Field(None, description="ID do usuário que fez upload")
    tags: Optional[List[str]] = Field(None, description="Tags para filtrar")
    date_from: Optional[datetime] = Field(None, description="Data de início para filtrar")
    date_to: Optional[datetime] = Field(None, description="Data de fim para filtrar")
    page: int = Field(1, ge=1, description="Número da página")
    size: int = Field(20, ge=1, le=100, description="Tamanho da página")


class FileStatistics(BaseModel):
    """Schema para estatísticas de arquivos"""
    total_files: int = Field(..., description="Total de arquivos")
    total_size: int = Field(..., description="Tamanho total em bytes")
    files_by_type: dict = Field(..., description="Contagem de arquivos por tipo")
    files_by_project: dict = Field(..., description="Contagem de arquivos por projeto")
    recent_uploads: List[FileDetailResponse] = Field(..., description="Uploads recentes")
    
    class Config:
        from_attributes = True


class FilePreview(BaseModel):
    """Schema para preview de arquivo"""
    id: int = Field(..., description="ID do arquivo")
    filename: str = Field(..., description="Nome do arquivo")
    file_type: str = Field(..., description="Tipo de arquivo")
    mime_type: str = Field(..., description="Tipo MIME")
    file_size: int = Field(..., description="Tamanho do arquivo")
    thumbnail_url: Optional[str] = Field(None, description="URL da miniatura (para imagens)")
    preview_url: Optional[str] = Field(None, description="URL do preview")
    can_preview: bool = Field(..., description="Se o arquivo pode ser visualizado")
    
    class Config:
        from_attributes = True


class FileUploadProgress(BaseModel):
    """Schema para progresso de upload"""
    file_id: Optional[int] = Field(None, description="ID do arquivo (quando concluído)")
    filename: str = Field(..., description="Nome do arquivo")
    bytes_uploaded: int = Field(..., description="Bytes já enviados")
    total_bytes: int = Field(..., description="Total de bytes")
    progress_percentage: float = Field(..., description="Percentual de progresso")
    status: str = Field(..., description="Status do upload (uploading, completed, error)")
    error_message: Optional[str] = Field(None, description="Mensagem de erro (se houver)")
    
    class Config:
        from_attributes = True
