from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CONFIGURATOR = "configurator"
    VIEWER = "viewer"

class AuthProvider(str, Enum):
    PASSWORD = "password"
    GOOGLE = "google"
    GITHUB = "github" 