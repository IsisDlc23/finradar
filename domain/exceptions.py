class AppError(Exception):
    pass


class DataLoaderError(AppError):
    pass


class RepositoryError(AppError):
    pass


class AnalysisError(AppError):
    pass
