class AnalysisResult:

    def __init__(self, name: str, metrics: dict = None, rows: list = None):
        self.name = name
        self.metrics = metrics or {}
        self.rows = rows or []

    def is_empty(self) -> bool:
        return not self.metrics and not self.rows

    def __repr__(self) -> str:
        return f"AnalysisResult(name='{self.name}', metrics={len(self.metrics)}, rows={len(self.rows)})"