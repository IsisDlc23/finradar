class AppError(Exception):
    """Clase base para errores de la aplicación."""
    pass

class RepositoryError(AppError):
    """Exepción para errores en la capa de acceso a datos."""
    pass
