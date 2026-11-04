from datetime import timedelta
from typing import List

from analysis.analysis_result import AnalysisResult
from analysis.analysis_strategy import AnalysisStrategy
from domain.transaction import Transaction


class RFMSegmentationStrategy(AnalysisStrategy):

    @property
    def name(self) -> str:
        return "rfm"

    def analyze(self, data: List[Transaction]) -> AnalysisResult:
        approved = [t for t in data if t.status == "Aprobada" and t.transaction_date]
        if not approved:
            return AnalysisResult(self.name)

        reference = max(t.transaction_date for t in approved) + timedelta(days=1)
        customers = {}
        for t in approved:
            c = customers.setdefault(t.customer_id, {"last": t.transaction_date, "frequency": 0, "monetary": 0.0})
            c["last"] = max(c["last"], t.transaction_date)
            c["frequency"] += 1
            c["monetary"] += t.amount

        rows = []
        for customer_id, c in customers.items():
            rows.append({
                "customer_id": customer_id,
                "recency_days": (reference - c["last"]).days,
                "frequency": c["frequency"],
                "monetary": round(c["monetary"], 2),
            })

        self._score(rows, "recency_days", "r_score", reverse=True)
        self._score(rows, "frequency", "f_score")
        self._score(rows, "monetary", "m_score")
        for row in rows:
            row["segment"] = self._segment(row["r_score"], (row["f_score"] + row["m_score"]) / 2)

        segments = {}
        for row in rows:
            segments[row["segment"]] = segments.get(row["segment"], 0) + 1
        metrics = {"customers": len(rows), **{f"segment_{k}": v for k, v in segments.items()}}
        return AnalysisResult(self.name, metrics, rows)

    @staticmethod
    def _score(rows, field, score_field, reverse=False):
        ordered = sorted(rows, key=lambda r: r[field], reverse=reverse)
        size = len(ordered)
        for position, row in enumerate(ordered):
            row[score_field] = 1 + position * 5 // size

    @staticmethod
    def _segment(r, fm):
        if r >= 4 and fm >= 4:
            return "Campeones"
        if r >= 3 and fm >= 3:
            return "Leales"
        if r >= 4:
            return "Potenciales"
        if r <= 2 and fm >= 3:
            return "En riesgo"
        if r == 3:
            return "Necesitan atencion"
        if fm >= 2:
            return "Hibernando"
        return "Perdidos"