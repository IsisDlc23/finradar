class Customer:
 
    def __init__(
        self,
        customer_id: str,
        customer_name: str,
        customer_age: int,
        customer_gender: str,
        province: str,
        account_type: str,
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_age = customer_age
        self.customer_gender = customer_gender
        self.province = province
        self.account_type = account_type
 
    def __repr__(self) -> str:
        return (
            f"Customer(id='{self.customer_id}', "
            f"name='{self.customer_name}', "
            f"province='{self.province}')"
        )
 