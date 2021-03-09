from enum import Enum, unique

@unique
class RoleType(Enum):
    ADMINISTRATOR = 1
    USER = 2
