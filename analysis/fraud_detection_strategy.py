from statistics import mean, pstdev
from typing import List

from analysis.analysis_result import AnalysisResult
from analysis.analysis_strategy import AnalysisStrategy
from domain.transaction import Transaction


class FraudDetectionStrategy(AnalysisStrategy):

    def __init__(self, z_limit: float = 3.0):
        self._z_limit = z_limit

    @property
    def name(self) -> str:
        return "fraud"

    def analyze(self, data: List[Transaction]) -> AnalysisResult:
        if len(data) < 2:
            return AnalysisResult(self.name)

        amounts = [t.amount for t in data]
        avg = mean(amounts)
        std = pstdev(amounts) or 1.0

        suspicious = []
        for t in data:
            z_score = (t.amount - avg) / std
            reasons = []
            if t.is_high_amount():
                reasons.append("monto_alto")
            if t.is_international == 1:
                reasons.append("internacional")
            if z_score > self._z_limit:
                reasons.append("z_score")
            if reasons:
                suspicious.append({
                    "transaction_id": t.transaction_id,
                    "customer_id": t.customer_id,
                    "amount": t.amount,
                    "channel": t.channel,
                    "z_score": round(z_score, 2),
                    "reasons": ",".join(reasons),
                    "is_fraud": t.is_fraud,
                })

        total = len(data)
        frauds = sum(t.is_fraud for t in data)
        detected = sum(row["is_fraud"] for row in suspicious)
        metrics = {
            "total_transactions": total,
            "marked_as_fraud": frauds,
            "fraud_rate_pct": round(100 * frauds / total, 4),
            "suspicious": len(suspicious),
            "fraud_detected": detected,
            "detection_rate_pct": round(100 * detected / frauds, 2) if frauds else 0.0,
            "average_amount": round(avg, 2),
            "std_amount": round(std, 2),
        }
        return AnalysisResult(self.name, metrics, suspicious)