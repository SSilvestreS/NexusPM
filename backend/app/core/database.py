"""
Configuração e gerenciamento do banco de dados
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import asyncpg
from typing import AsyncGenerator
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Configuração do engine assíncrono
async_engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
    max_overflow=20,
    pool_size=10
)

# Engine síncrono para migrações
engine = create_async_engine(
    settings.database_url.replace("+asyncpg", ""),
    echo=settings.debug
)

# Configuração das sessões
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False
)

# Base para os modelos
Base = declarative_base()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessão assíncrona do banco
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error("Erro na sessão do banco", error=str(e))
            await session.rollback()
            raise
        finally:
            await session.close()


def get_db():
    """
    Dependency para obter sessão síncrona do banco
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error("Erro na sessão do banco", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


async def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    try:
        async with async_engine.begin() as conn:
            # Criar todas as tabelas
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tabelas do banco de dados criadas com sucesso")
            
            # Verificar se as tabelas foram criadas
            result = await conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = [row[0] for row in result.fetchall()]
            logger.info("Tabelas criadas", tables=tables)
            
    except Exception as e:
        logger.error("Erro ao inicializar banco de dados", error=str(e))
        raise


async def check_db_health() -> bool:
    """
    Verifica a saúde do banco de dados
    """
    try:
        async with async_engine.begin() as conn:
            # Executar query simples para verificar conectividade
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
            
            # Verificar se as tabelas principais existem
            result = await conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            
            table_count = result.scalar()
            if table_count == 0:
                logger.warning("Nenhuma tabela encontrada no banco")
                return False
            
            logger.info("Banco de dados está saudável", table_count=table_count)
            return True
            
    except Exception as e:
        logger.error("Erro ao verificar saúde do banco", error=str(e))
        return False


async def close_db_connections():
    """
    Fecha todas as conexões do banco de dados
    """
    try:
        await async_engine.dispose()
        logger.info("Conexões do banco de dados fechadas")
    except Exception as e:
        logger.error("Erro ao fechar conexões do banco", error=str(e))


async def get_db_info():
    """
    Obtém informações sobre o banco de dados
    """
    try:
        async with async_engine.begin() as conn:
            # Informações da versão
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            
            # Informações das tabelas
            result = await conn.execute(text("""
                SELECT 
                    table_name,
                    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
                FROM information_schema.tables t
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables_info = [
                {"name": row[0], "columns": row[1]} 
                for row in result.fetchall()
            ]
            
            # Estatísticas do banco
            result = await conn.execute(text("""
                SELECT 
                    schemaname,
                    tablename,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables
                ORDER BY n_tup_ins + n_tup_upd + n_tup_del DESC
            """))
            
            stats = [
                {
                    "schema": row[0],
                    "table": row[1],
                    "inserts": row[2],
                    "updates": row[3],
                    "deletes": row[4]
                }
                for row in result.fetchall()
            ]
            
            return {
                "version": version,
                "tables": tables_info,
                "statistics": stats,
                "connection_pool": {
                    "size": async_engine.pool.size(),
                    "checked_in": async_engine.pool.checkedin(),
                    "checked_out": async_engine.pool.checkedout(),
                    "overflow": async_engine.pool.overflow()
                }
            }
            
    except Exception as e:
        logger.error("Erro ao obter informações do banco", error=str(e))
        return None


async def reset_db():
    """
    Reseta o banco de dados (CUIDADO: isso apaga todos os dados!)
    """
    try:
        async with async_engine.begin() as conn:
            # Desabilitar verificações de chave estrangeira
            await conn.execute(text("SET session_replication_role = replica"))
            
            # Dropar todas as tabelas
            await conn.run_sync(Base.metadata.drop_all)
            
            # Reabilitar verificações de chave estrangeira
            await conn.execute(text("SET session_replication_role = DEFAULT"))
            
            # Recriar todas as tabelas
            await conn.run_sync(Base.metadata.create_all)
            
            logger.warning("Banco de dados foi resetado completamente")
            
    except Exception as e:
        logger.error("Erro ao resetar banco de dados", error=str(e))
        raise


async def backup_db(backup_path: str):
    """
    Cria um backup do banco de dados
    """
    try:
        import subprocess
        import os
        
        # Comando para backup usando pg_dump
        cmd = [
            "pg_dump",
            "-h", settings.database_host,
            "-U", settings.database_user,
            "-d", settings.database_name,
            "-f", backup_path,
            "--format=custom",
            "--verbose"
        ]
        
        # Definir variável de ambiente para senha
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.database_password
        
        # Executar comando
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info("Backup do banco criado com sucesso", path=backup_path)
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error("Erro ao criar backup", error=str(e), stderr=e.stderr)
        return False
    except Exception as e:
        logger.error("Erro inesperado ao criar backup", error=str(e))
        return False


async def restore_db(backup_path: str):
    """
    Restaura o banco de dados a partir de um backup
    """
    try:
        import subprocess
        import os
        
        # Comando para restore usando pg_restore
        cmd = [
            "pg_restore",
            "-h", settings.database_host,
            "-U", settings.database_user,
            "-d", settings.database_name,
            "--clean",
            "--if-exists",
            "--verbose",
            backup_path
        ]
        
        # Definir variável de ambiente para senha
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.database_password
        
        # Executar comando
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info("Banco de dados restaurado com sucesso", path=backup_path)
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error("Erro ao restaurar banco", error=str(e), stderr=e.stderr)
        return False
    except Exception as e:
        logger.error("Erro inesperado ao restaurar banco", error=str(e))
        return False
