from enum import Enum

class UserRoleEnum(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    MEMBER = 'member'

class TaskPriorityEnum(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'