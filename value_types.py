from enum import Enum



class UserRole(str, Enum):
    USER = 'user'
    ADMIN = 'admin'


class ProfileType(str, Enum):
    ENGINEER = 'engineer'
    PARTNER = 'partner'