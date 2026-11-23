from typing import Dict, Type

from analysis.analysis_strategy import AnalysisStrategy
from analysis.fraud_detection_strategy import FraudDetectionStrategy
from analysis.rfm_segmentation_strategy import RFMSegmentationStrategy
from domain.exceptions import AnalysisError


class AnalysisStrategyFactory:

    _registry: Dict[str, Type[AnalysisStrategy]] = {
        "fraud": FraudDetectionStrategy,
        "rfm": RFMSegmentationStrategy,
    }

    @classmethod
    def create(cls, kind: str) -> AnalysisStrategy:
        try:
            return cls._registry[kind]()
        except KeyError:
            raise AnalysisError(f"Tipo de analisis no soportado: {kind}")

    @classmethod
    def register(cls, kind: str, strategy_class: Type[AnalysisStrategy]) -> None:
        cls._registry[kind] = strategy_class

    @classmethod
    def available(cls) -> list:
        return sorted(cls._registry)