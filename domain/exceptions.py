class AppError(Exception):
    pass


class DataLoadError(AppError):
    pass


class RepositoryError(AppError):
    pass


class AnalysisError(AppError):
    pass
