"""
Schemas Pydantic para validação de dados
"""
from .auth import *
from .user import *
from .project import *
from .task import *
from .comment import *
from .notification import *
from .search import *
from .file import *

__all__ = [
    # Auth schemas
    "UserRegister",
    "UserLogin", 
    "TokenResponse",
    "PasswordReset",
    "PasswordResetConfirm",
    "OAuthLogin",
    "ChangePassword",
    "UserProfileUpdate",
    "EmailVerification",
    "ResendVerification",
    
    # User schemas
    "UserStatus",
    "UserRole",
    "Theme",
    "Language",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserProfileUpdate",
    "UserResponse",
    "UserDetailResponse",
    "UserPreferenceUpdate",
    "UserPreferenceResponse",
    "UserSessionResponse",
    "ChangePassword",
    "UserListResponse",
    "UserSearchQuery",
    
    # Project schemas
    "ProjectStatus",
    "ProjectPriority",
    "ProjectVisibility",
    "MemberRole",
    "ProjectBase",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectDetailResponse",
    "ProjectListResponse",
    "ProjectSearchQuery",
    "ProjectMemberBase",
    "ProjectMemberCreate",
    "ProjectMemberUpdate",
    "ProjectMemberResponse",
    "ProjectMemberListResponse",
    "ProjectVersionBase",
    "ProjectVersionCreate",
    "ProjectVersionUpdate",
    "ProjectVersionResponse",
    "ProjectFileBase",
    "ProjectFileCreate",
    "ProjectFileUpdate",
    "ProjectFileResponse",
    "ProjectTemplateBase",
    "ProjectTemplateCreate",
    "ProjectTemplateUpdate",
    "ProjectTemplateResponse",
    
    # Task schemas
    "TaskStatus",
    "TaskPriority",
    "TaskType",
    "TaskBase",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskDetailResponse",
    "TaskListResponse",
    "TaskSearchQuery",
    "TimeLogBase",
    "TimeLogCreate",
    "TimeLogUpdate",
    "TimeLogResponse",
    "TaskAttachmentBase",
    "TaskAttachmentCreate",
    "TaskAttachmentUpdate",
    "TaskAttachmentResponse",
    "TaskDependencyBase",
    "TaskDependencyCreate",
    "TaskDependencyResponse",
    "TaskBulkUpdate",
    "TaskStatistics",
    
    # Comment schemas
    "CommentStatus",
    "ReactionType",
    "CommentBase",
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    "CommentDetailResponse",
    "CommentListResponse",
    "CommentSearchQuery",
    "CommentReactionBase",
    "CommentReactionCreate",
    "CommentReactionUpdate",
    "CommentReactionResponse",
    "CommentReactionSummary",
    "CommentEditBase",
    "CommentEditCreate",
    "CommentEditResponse",
    "CommentMention",
    "CommentThreadResponse",
    "CommentBulkAction",
    "CommentNotification",
    "CommentStatistics",
    
    # Notification schemas
    "NotificationType",
    "NotificationPriority",
    "NotificationStatus",
    "NotificationChannel",
    "NotificationBase",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
    "NotificationDetailResponse",
    "NotificationListResponse",
    "NotificationSearchQuery",
    "NotificationPreferenceBase",
    "NotificationPreferenceCreate",
    "NotificationPreferenceUpdate",
    "NotificationPreferenceResponse",
    "NotificationTypePreferenceBase",
    "NotificationTypePreferenceCreate",
    "NotificationTypePreferenceUpdate",
    "NotificationTypePreferenceResponse",
    "NotificationTemplateBase",
    "NotificationTemplateCreate",
    "NotificationTemplateUpdate",
    "NotificationTemplateResponse",
    "NotificationBulkAction",
    "NotificationDeliveryStatus",
                "NotificationStatistics",
            
            # Search schemas
            "SearchQuery",
            "SearchResult",
            "SearchResponse",
            "SearchSuggestion",
            "SearchFilters",
            "SearchStatistics",
            
            # File schemas
            "FileMetadata",
            "FileUploadResponse",
            "FileUpdateRequest",
            "FileDetailResponse",
            "FileListResponse",
            "FileSearchQuery",
            "FileStatistics",
            "FilePreview",
            "FileUploadProgress",
        ]


def get_all_schemas():
    """Retorna todos os schemas disponíveis"""
    return __all__
