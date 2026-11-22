from typing import Dict, List, Type

from analysis.analysis_strategy import AnalysisStrategy
from analysis.fraud_detection_strategy import FraudDetectionStrategy
from analysis.monthly_trend_strategy import MonthlyTrendStrategy
from analysis.rfm_segmentation_strategy import RFMSegmentationStrategy
from domain.exceptions import AnalysisError


class AnalysisStrategyFactory:

    _registry: Dict[str, Type[AnalysisStrategy]] = {
        "fraud": FraudDetectionStrategy,
        "rfm": RFMSegmentationStrategy,
        "trend": MonthlyTrendStrategy,
    }

    @classmethod
    def create(cls, kind: str) -> AnalysisStrategy:
        try:
            return cls._registry[kind]()
        except KeyError:
            raise AnalysisError(f"Tipo de analisis no soportado: {kind}")

    @classmethod
    def register(cls, kind: str, strategy: Type[AnalysisStrategy]) -> None:
        cls._registry[kind] = strategy

    @classmethod
    def available(cls) -> List[str]:
        return list(cls._registry)