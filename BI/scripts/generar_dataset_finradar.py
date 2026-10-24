# scripts/generate_dataset.py
import csv, random
from datetime import datetime, timedelta
from faker import Faker
 
SEED = 42
TOTAL_ROWS = 1_000_000
OUTPUT_PATH = "data/transactions.csv"
 
Faker.seed(SEED)
random.seed(SEED)
fake = Faker("es_MX")
 
CATEGORIES = ["supermercado", "restaurante", "combustible", "tecnologia", "viajes", "farmacia"]
CHANNELS = ["pos", "online", "atm"]
CITIES = ["Panamá", "Colón", "David", "Santiago", "Chitré"]
START = datetime(2025, 1, 1)
 
def build_transaction(index: int) -> dict:
    is_fraud = random.random() < 0.02                  # ~2 % de casos sospechosos
    amount = round(random.lognormvariate(3.5, 0.9), 2)  # muchos montos bajos, pocos altos
    if is_fraud:
        amount = round(amount * random.uniform(3, 8), 2)
    return {
        "transaction_id": f"TX-{index:07d}",
        "customer_id": f"C-{random.randint(1, 5000):05d}",
        "customer_name": fake.name(),
        "amount": amount,
        "currency": "USD",
        "timestamp": (START + timedelta(minutes=random.randint(0, 525_600))).isoformat(),
        "merchant_category": random.choice(CATEGORIES),
        "channel": random.choice(CHANNELS),
        "city": random.choice(CITIES),
        "is_fraud": is_fraud,
    }
 
def main() -> None:
    rows = [build_transaction(i) for i in range(1, TOTAL_ROWS + 1)]
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Filas generadas: {len(rows)}")
 
if __name__ == "__main__":
    main()
 