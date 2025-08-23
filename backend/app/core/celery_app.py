"""
Celery configuration for background tasks
"""

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "nova_pasta",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.project_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.export_tasks",
        "app.tasks.search_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.email_tasks.*": {"queue": "email"},
        "app.tasks.project_tasks.*": {"queue": "projects"},
        "app.tasks.notification_tasks.*": {"queue": "notifications"},
        "app.tasks.export_tasks.*": {"queue": "exports"},
        "app.tasks.search_tasks.*": {"queue": "search"},
    },
    
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_always_eager=False,
    task_eager_propagates=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "app.tasks.auth_tasks.cleanup_expired_sessions",
            "schedule": 3600.0,  # Every hour
        },
        "cleanup-old-notifications": {
            "task": "app.tasks.notification_tasks.cleanup_old_notifications",
            "schedule": 86400.0,  # Every day
        },
        "update-search-index": {
            "task": "app.tasks.search_tasks.update_search_index",
            "schedule": 300.0,  # Every 5 minutes
        },
        "send-reminder-emails": {
            "task": "app.tasks.email_tasks.send_reminder_emails",
            "schedule": 3600.0,  # Every hour
        },
    },
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,  # 10 minutes
    
    # Retry configuration
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_remote_tracebacks=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Security
    security_key=settings.SECRET_KEY,
    security_certificate=None,
    security_cert_store=None,
)

# Task error handling
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing"""
    print(f"Request: {self.request!r}")

# Health check task
@celery_app.task
def health_check():
    """Health check task for monitoring"""
    return {"status": "healthy", "service": "celery"}

# Task monitoring
@celery_app.task
def get_queue_stats():
    """Get queue statistics for monitoring"""
    from celery.task.control import inspect
    
    i = inspect()
    stats = i.stats()
    active = i.active()
    reserved = i.reserved()
    
    return {
        "stats": stats,
        "active": active,
        "reserved": reserved
    }
