from datetime import date, datetime
from typing import Optional
 
 
class Transaction:
 
    HIGH_AMOUNT = 3000.0
 
    def __init__(
        self,
        transaction_id: str,
        customer_id: str,
        amount: float,
        merchant_category: str,
        channel: str,
        is_international: int,
        status: str,
        is_fraud: int,
        transaction_date: Optional[date] = None,
        transaction_time: Optional[str] = None,
        card_type: Optional[str] = None,
        currency: str = "PAB",
    ):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.amount = float(amount)
        self.merchant_category = merchant_category
        self.channel = channel
        self.is_international = int(is_international)
        self.status = status
        self.is_fraud = int(is_fraud)
        self.transaction_date = transaction_date
        self.transaction_time = transaction_time
        self.card_type = card_type
        self.currency = currency
 
    def is_high_amount(self) -> bool:
        return self.amount > self.HIGH_AMOUNT
 
    def is_marked_as_fraud(self) -> bool:
        return self.is_fraud == 1
 
    @classmethod
    def from_document(cls, doc: dict) -> "Transaction":
        fecha = doc.get("transaction_date")
        if isinstance(fecha, datetime):
            fecha = fecha.date()
        elif isinstance(fecha, str):
            fecha = date.fromisoformat(fecha[:10])
        return cls(
            transaction_id=doc["transaction_id"],
            customer_id=doc["customer_id"],
            amount=doc["amount"],
            merchant_category=doc["merchant_category"],
            channel=doc["channel"],
            is_international=int(doc.get("is_international", 0)),
            status=doc["status"],
            is_fraud=int(doc.get("is_fraud", 0)),
            transaction_date=fecha,
            transaction_time=doc.get("transaction_time"),
            card_type=doc.get("card_type"),
            currency=doc.get("currency", "PAB"),
        )
 
    def to_document(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "amount": self.amount,
            "merchant_category": self.merchant_category,
            "channel": self.channel,
            "is_international": bool(self.is_international),
            "status": self.status,
            "is_fraud": bool(self.is_fraud),
            "transaction_date": (
                datetime.combine(self.transaction_date, datetime.min.time())
                if self.transaction_date
                else None
            ),
            "transaction_time": self.transaction_time,
            "card_type": self.card_type,
            "currency": self.currency,
        }
 
    def __repr__(self) -> str:
        return (
            f"Transaction(id='{self.transaction_id}', "
            f"customer='{self.customer_id}', "
            f"amount={self.amount}, "
            f"date={self.transaction_date}, "
            f"status='{self.status}')"
        )