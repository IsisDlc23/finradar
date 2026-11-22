from collections import defaultdict
from typing import List

from analysis.analysis_result import AnalysisResult
from analysis.analysis_strategy import AnalysisStrategy
from domain.transaction import Transaction


class MonthlyTrendStrategy(AnalysisStrategy):
    @property
    def name(self) -> str:
        return "trend"

    def analyze(self, data: List[Transaction]) -> AnalysisResult:
        dated = [t for t in data if t.transaction_date is not None]
        if not dated:
            return AnalysisResult(self.name)

        totals = defaultdict(lambda: {"transactions": 0, "amount": 0.0, "frauds": 0})
        for transaction in dated:
            month = transaction.transaction_date.strftime("%Y-%m")
            totals[month]["transactions"] += 1
            totals[month]["amount"] += transaction.amount
            totals[month]["frauds"] += transaction.is_fraud

        rows = []
        previous_amount = None
        for month in sorted(totals):
            values = totals[month]
            amount = round(values["amount"], 2)
            change = None
            if previous_amount:
                change = round((amount - previous_amount) / previous_amount * 100, 2)
            rows.append({
                "month": month,
                "transactions": values["transactions"],
                "amount": amount,
                "average_ticket": round(amount / values["transactions"], 2),
                "frauds": values["frauds"],
                "fraud_rate_pct": round(values["frauds"] / values["transactions"] * 100, 3),
                "change_pct": change,
            })
            previous_amount = amount

        best = max(rows, key=lambda row: row["amount"])
        worst = min(rows, key=lambda row: row["amount"])
        total_amount = round(sum(row["amount"] for row in rows), 2)
        metrics = {
            "months": len(rows),
            "total_amount": total_amount,
            "average_monthly_amount": round(total_amount / len(rows), 2),
            "best_month": best["month"],
            "worst_month": worst["month"],
            "variation_pct": round((best["amount"] - worst["amount"]) / worst["amount"] * 100, 2),
        }
        return AnalysisResult(self.name, metrics=metrics, rows=rows)