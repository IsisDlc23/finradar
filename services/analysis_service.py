import logging

from analysis.analysis_result import AnalysisResult
from analysis.strategy_factory import AnalysisStrategyFactory

logger = logging.getLogger(__name__)


class AnalysisService:

    def __init__(self, repository, factory=AnalysisStrategyFactory):
        self._repository = repository
        self._factory = factory

    def run(self, kind: str, filters: dict = None, limit: int = 50_000) -> AnalysisResult:
        strategy = self._factory.create(kind)
        logger.info("Ejecutando analisis '%s' sobre %d transacciones", kind, limit)
        data = self._repository.find_by_filter(filters or {}, limit=limit)
        if not data:
            logger.warning("No hay transacciones para analizar")
        result = strategy.analyze(data)
        logger.info("Analisis '%s' terminado", kind)
        return result