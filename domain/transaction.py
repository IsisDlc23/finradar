class Transaction:

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
    ):
        self.transaction_id = transaction_id
        self.customer_id = customer_id
        self.amount = amount
        self.merchant_category = merchant_category
        self.channel = channel
        self.is_international = is_international
        self.status = status
        self.is_fraud = is_fraud

    def __repr__(self) -> str:
        return (
            f"Transaction(id='{self.transaction_id}', "
            f"customer='{self.customer_id}', "
            f"amount={self.amount}, "
            f"status='{self.status}')"
        )