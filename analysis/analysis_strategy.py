from abc import ABC, abstractmethod
from typing import List

from analysis.analysis_result import AnalysisResult
from domain.transaction import Transaction


class AnalysisStrategy(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def analyze(self, data: List[Transaction]) -> AnalysisResult:
        ...