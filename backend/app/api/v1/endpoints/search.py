"""
Endpoints para busca full-text
"""
from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, text
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.models.task import Task
from app.models.comment import Comment
from app.schemas.search import SearchQuery, SearchResult, SearchResponse

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Termo de busca"),
    entity_type: Optional[str] = Query(None, description="Tipo de entidade (project, task, comment, all)"),
    project_id: Optional[int] = Query(None, description="Limitar busca a um projeto específico"),
    author_id: Optional[int] = Query(None, description="Limitar busca por autor"),
    date_from: Optional[str] = Query(None, description="Data de início (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Data de fim (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(20, ge=1, le=100, description="Tamanho da página"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Busca full-text em projetos, tarefas e comentários
    """
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Termo de busca não pode estar vazio"
        )
    
    # Normalizar termo de busca
    search_term = f"%{q.strip().lower()}%"
    
    # Lista para armazenar resultados
    all_results = []
    
    # Buscar em projetos
    if entity_type in [None, "all", "project"]:
        project_query = select(Project).options(
            selectinload(Project.owner),
            selectinload(Project.members)
        ).where(
            and_(
                Project.is_deleted == False,
                or_(
                    Project.name.ilike(search_term),
                    Project.description.ilike(search_term),
                    Project.tags.contains([q])
                )
            )
        )
        
        # Filtrar por projeto específico
        if project_id:
            project_query = project_query.where(Project.id == project_id)
        
        # Filtrar por data
        if date_from:
            project_query = project_query.where(Project.created_at >= date_from)
        if date_to:
            project_query = project_query.where(Project.created_at <= date_to)
        
        projects = await db.execute(project_query)
        projects = projects.scalars().all()
        
        # Verificar permissões de acesso
        accessible_projects = []
        for project in projects:
            # Verificar se o usuário é membro
            member = await db.execute(
                select(ProjectMember).where(
                    and_(
                        ProjectMember.project_id == project.id,
                        ProjectMember.user_id == current_user.id
                    )
                )
            )
            if member.scalar_one_or_none():
                accessible_projects.append(project)
        
        # Adicionar resultados de projetos
        for project in accessible_projects:
            all_results.append(SearchResult(
                id=project.id,
                entity_type="project",
                title=project.name,
                content=project.description or "",
                author=project.owner.name,
                author_id=project.owner.id,
                created_at=project.created_at,
                updated_at=project.updated_at,
                project_id=project.id,
                relevance_score=calculate_relevance_score(project.name, project.description, q)
            ))
    
    # Buscar em tarefas
    if entity_type in [None, "all", "task"]:
        task_query = select(Task).options(
            selectinload(Task.assignee),
            selectinload(Task.project)
        ).where(
            and_(
                Task.is_deleted == False,
                or_(
                    Task.name.ilike(search_term),
                    Task.description.ilike(search_term),
                    Task.tags.contains([q])
                )
            )
        )
        
        # Filtrar por projeto específico
        if project_id:
            task_query = task_query.where(Task.project_id == project_id)
        
        # Filtrar por autor
        if author_id:
            task_query = task_query.where(Task.created_by == author_id)
        
        # Filtrar por data
        if date_from:
            task_query = task_query.where(Task.created_at >= date_from)
        if date_to:
            task_query = task_query.where(Task.created_at <= date_to)
        
        tasks = await db.execute(task_query)
        tasks = tasks.scalars().all()
        
        # Verificar permissões de acesso
        accessible_tasks = []
        for task in tasks:
            # Verificar se o usuário tem acesso ao projeto da tarefa
            member = await db.execute(
                select(ProjectMember).where(
                    and_(
                        ProjectMember.project_id == task.project_id,
                        ProjectMember.user_id == current_user.id
                    )
                )
            )
            if member.scalar_one_or_none():
                accessible_tasks.append(task)
        
        # Adicionar resultados de tarefas
        for task in accessible_tasks:
            all_results.append(SearchResult(
                id=task.id,
                entity_type="task",
                title=task.name,
                content=task.description or "",
                author=task.assignee.name if task.assignee else "Não atribuído",
                author_id=task.created_by,
                created_at=task.created_at,
                updated_at=task.updated_at,
                project_id=task.project_id,
                task_id=task.id,
                relevance_score=calculate_relevance_score(task.name, task.description, q)
            ))
    
    # Buscar em comentários
    if entity_type in [None, "all", "comment"]:
        comment_query = select(Comment).options(
            selectinload(Comment.author),
            selectinload(Comment.project),
            selectinload(Comment.task)
        ).where(
            and_(
                Comment.status == "active",
                Comment.content.ilike(search_term)
            )
        )
        
        # Filtrar por projeto específico
        if project_id:
            comment_query = comment_query.where(Comment.project_id == project_id)
        
        # Filtrar por autor
        if author_id:
            comment_query = comment_query.where(Comment.author_id == author_id)
        
        # Filtrar por data
        if date_from:
            comment_query = comment_query.where(Comment.created_at >= date_from)
        if date_to:
            comment_query = comment_query.where(Comment.created_at <= date_to)
        
        comments = await db.execute(comment_query)
        comments = comments.scalars().all()
        
        # Verificar permissões de acesso
        accessible_comments = []
        for comment in comments:
            project_id_comment = comment.project_id
            if comment.task_id:
                # Se for comentário de tarefa, buscar o projeto da tarefa
                task = await db.execute(
                    select(Task).where(Task.id == comment.task_id)
                )
                task = task.scalar_one_or_none()
                if task:
                    project_id_comment = task.project_id
            
            if project_id_comment:
                member = await db.execute(
                    select(ProjectMember).where(
                        and_(
                            ProjectMember.project_id == project_id_comment,
                            ProjectMember.user_id == current_user.id
                        )
                    )
                )
                if member.scalar_one_or_none():
                    accessible_comments.append(comment)
        
        # Adicionar resultados de comentários
        for comment in accessible_comments:
            project_id_comment = comment.project_id
            task_id_comment = comment.task_id
            
            if comment.task_id:
                task = await db.execute(
                    select(Task).where(Task.id == comment.task_id)
                )
                task = task.scalar_one_or_none()
                if task:
                    project_id_comment = task.project_id
            
            all_results.append(SearchResult(
                id=comment.id,
                entity_type="comment",
                title=f"Comentário em {'Tarefa' if comment.task_id else 'Projeto'}",
                content=comment.content,
                author=comment.author.name,
                author_id=comment.author.id,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                project_id=project_id_comment,
                task_id=task_id_comment,
                comment_id=comment.id,
                relevance_score=calculate_relevance_score("", comment.content, q)
            ))
    
    # Ordenar por relevância e data
    all_results.sort(key=lambda x: (x.relevance_score, x.created_at), reverse=True)
    
    # Aplicar paginação
    total = len(all_results)
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    paginated_results = all_results[start_idx:end_idx]
    
    return SearchResponse(
        items=paginated_results,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
        query=q,
        entity_type=entity_type or "all"
    )


@router.get("/suggestions", response_model=List[str])
async def get_search_suggestions(
    q: str = Query(..., description="Termo de busca parcial"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de sugestões"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Obter sugestões de busca baseadas no termo parcial
    """
    if len(q.strip()) < 2:
        return []
    
    search_term = f"%{q.strip().lower()}%"
    suggestions = set()
    
    # Buscar sugestões em projetos
    project_suggestions = await db.execute(
        select(Project.name).where(
            and_(
                Project.is_deleted == False,
                Project.name.ilike(search_term)
            )
        ).limit(limit)
    )
    for suggestion in project_suggestions.scalars():
        suggestions.add(suggestion)
    
    # Buscar sugestões em tarefas
    task_suggestions = await db.execute(
        select(Task.name).where(
            and_(
                Task.is_deleted == False,
                Task.name.ilike(search_term)
            )
        ).limit(limit)
    )
    for suggestion in task_suggestions.scalars():
        suggestions.add(suggestion)
    
    # Buscar sugestões em tags
    tag_suggestions = await db.execute(
        select(Project.tags).where(
            and_(
                Project.is_deleted == False,
                Project.tags.overlap([q])
            )
        ).limit(limit)
    )
    for tags in tag_suggestions.scalars():
        if tags:
            for tag in tags:
                if q.lower() in tag.lower():
                    suggestions.add(tag)
    
    # Converter para lista e ordenar
    suggestions_list = list(suggestions)
    suggestions_list.sort()
    
    return suggestions_list[:limit]


@router.get("/advanced", response_model=SearchResponse)
async def advanced_search(
    query: SearchQuery,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Busca avançada com múltiplos critérios
    """
    # Implementar busca avançada com filtros complexos
    # Esta é uma versão simplificada - pode ser expandida conforme necessário
    
    if not query.terms and not query.exact_phrase and not query.tags:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deve especificar pelo menos um critério de busca"
        )
    
    # Construir query de busca baseada nos critérios
    search_terms = []
    
    if query.terms:
        search_terms.extend(query.terms)
    
    if query.exact_phrase:
        search_terms.append(query.exact_phrase)
    
    if query.tags:
        search_terms.extend(query.tags)
    
    # Usar a busca básica com os termos combinados
    combined_query = " ".join(search_terms)
    
    # Chamar a busca básica
    return await search(
        q=combined_query,
        entity_type=query.entity_type,
        project_id=query.project_id,
        author_id=query.author_id,
        date_from=query.date_from,
        date_to=query.date_to,
        page=query.page,
        size=query.size,
        current_user=current_user,
        db=db
    )


def calculate_relevance_score(title: str, content: str, search_term: str) -> float:
    """
    Calcular pontuação de relevância para um resultado de busca
    """
    score = 0.0
    search_lower = search_term.lower()
    
    # Pontuação por título (mais importante)
    if title and search_lower in title.lower():
        score += 10.0
        # Bônus se for exata no início
        if title.lower().startswith(search_lower):
            score += 5.0
    
    # Pontuação por conteúdo
    if content and search_lower in content.lower():
        score += 5.0
        # Bônus por múltiplas ocorrências
        occurrences = content.lower().count(search_lower)
        score += min(occurrences * 0.5, 3.0)
    
    # Bônus por correspondência exata
    if title and search_term.lower() == title.lower():
        score += 15.0
    
    return score
