"""
generar_dataset_finradar.py
Generador de dataset ficticio para el proyecto FinRadar Panama S.A.
Genera transacciones financieras sinteticas para analisis de Big Data.

Uso:
    python generar_dataset_finradar.py

Salida:
    transacciones_finradar.csv  (1,000,000 de registros por defecto)

Requisitos:
    pip install numpy pandas
"""

import numpy as np
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuracion general
# ---------------------------------------------------------------------------
NUM_RECORDS = 1_000_000        # cantidad de transacciones a generar
NUM_CUSTOMERS = 40_000         # cantidad de clientes unicos
SEED = 2025                    # semilla para reproducibilidad
OUTPUT_FILE = "transacciones_finradar.csv"

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# Catalogos base (pools de valores)
# ---------------------------------------------------------------------------
provinces = np.array([
    "Panama", "Panama Oeste", "Colon", "Chiriqui", "Cocle",
    "Herrera", "Los Santos", "Veraguas", "Bocas del Toro", "Darien",
])
province_weights = np.array([0.42, 0.16, 0.08, 0.11, 0.06,
                             0.04, 0.03, 0.06, 0.02, 0.02])

account_types = np.array(["Ahorro", "Corriente", "Nomina", "Empresarial"])
account_weights = np.array([0.55, 0.20, 0.20, 0.05])

channels = np.array(["ATM", "POS", "Banca_en_linea", "App_movil", "Sucursal"])
channel_weights = np.array([0.22, 0.34, 0.14, 0.26, 0.04])

merchant_categories = np.array([
    "Supermercado", "Restaurante", "Combustible", "Farmacia", "Retail_ropa",
    "Electronica", "Salud", "Educacion", "Entretenimiento", "Viajes",
    "Servicios_publicos", "Transferencia", "Retiro_efectivo", "Comercio_online",
])
category_weights = np.array([0.18, 0.14, 0.10, 0.06, 0.07,
                             0.04, 0.05, 0.03, 0.05, 0.03,
                             0.06, 0.08, 0.07, 0.04])

card_types = np.array(["Debito", "Credito", "Prepago"])
card_weights = np.array([0.62, 0.33, 0.05])

genders = np.array(["F", "M"])
statuses = np.array(["Aprobada", "Rechazada", "Reversada"])
status_weights = np.array([0.93, 0.055, 0.015])

male_names = np.array([
    "Jose", "Luis", "Carlos", "Juan", "Miguel", "Ricardo", "Roberto",
    "Pedro", "Diego", "Andres", "Fernando", "Javier", "Alejandro", "Manuel",
])
female_names = np.array([
    "Ana", "Maria", "Rosa", "Carmen", "Yaritza", "Gabriela", "Lucia",
    "Daniela", "Sofia", "Valeria", "Camila", "Isabel", "Elena", "Patricia",
])
last_names = np.array([
    "Gonzalez", "Rodriguez", "Perez", "Sanchez", "Martinez", "Gomez",
    "Diaz", "Vargas", "Castillo", "Jimenez", "Moreno", "Herrera",
    "Cedeno", "Batista", "Quintero", "Espinosa", "Bethancourt", "Saldana",
])

# ---------------------------------------------------------------------------
# Generacion de clientes (dimension)
# ---------------------------------------------------------------------------
print(f"Generando {NUM_CUSTOMERS:,} clientes...")
cust_ids = np.array([f"CLI{n:06d}" for n in range(1, NUM_CUSTOMERS + 1)])
cust_gender = rng.choice(genders, NUM_CUSTOMERS)
# El nombre se elige del pool que corresponde al genero
cust_first = np.where(
    cust_gender == "F",
    rng.choice(female_names, NUM_CUSTOMERS),
    rng.choice(male_names, NUM_CUSTOMERS),
)
cust_last = rng.choice(last_names, NUM_CUSTOMERS)
cust_name = np.char.add(np.char.add(cust_first, " "), cust_last)
cust_age = rng.integers(18, 80, NUM_CUSTOMERS)
cust_province = rng.choice(provinces, NUM_CUSTOMERS, p=province_weights)
cust_account = rng.choice(account_types, NUM_CUSTOMERS, p=account_weights)

# ---------------------------------------------------------------------------
# Generacion de transacciones (hechos) - vectorizado
# ---------------------------------------------------------------------------
print(f"Generando {NUM_RECORDS:,} transacciones...")

# Cliente asociado a cada transaccion
idx = rng.integers(0, NUM_CUSTOMERS, NUM_RECORDS)

# Fechas: ultimos 365 dias
start = datetime(2024, 1, 1)
rand_seconds = rng.integers(0, 365 * 24 * 3600, NUM_RECORDS)
# Construimos fecha/hora de forma vectorizada con pandas (rapido para millones)
ts = pd.to_datetime(start) + pd.to_timedelta(rand_seconds, unit="s")

category = rng.choice(merchant_categories, NUM_RECORDS, p=category_weights)

# Monto: distribucion log-normal por categoria (montos realistas en Balboas)
base_mu = {
    "Supermercado": 3.4, "Restaurante": 2.9, "Combustible": 3.3,
    "Farmacia": 2.7, "Retail_ropa": 3.6, "Electronica": 5.2,
    "Salud": 4.1, "Educacion": 5.6, "Entretenimiento": 3.0,
    "Viajes": 6.0, "Servicios_publicos": 3.7, "Transferencia": 4.8,
    "Retiro_efectivo": 4.5, "Comercio_online": 3.8,
}
mu = np.array([base_mu[c] for c in category])
amount = np.round(rng.lognormal(mean=mu, sigma=0.6), 2)
amount = np.clip(amount, 1.0, 25_000.0)

channel = rng.choice(channels, NUM_RECORDS, p=channel_weights)
card_type = rng.choice(card_types, NUM_RECORDS, p=card_weights)
status = rng.choice(statuses, NUM_RECORDS, p=status_weights)
is_international = rng.choice([0, 1], NUM_RECORDS, p=[0.94, 0.06])

# Etiqueta de fraude (~0.4%). Correlacionada con montos altos + internacional
fraud_prob = 0.002 + 0.02 * (amount > 3000) + 0.03 * (is_international == 1)
is_fraud = (rng.random(NUM_RECORDS) < fraud_prob).astype(int)

print("Ensamblando DataFrame...")
df = pd.DataFrame({
    "transaction_id": [f"TXN{n:08d}" for n in range(1, NUM_RECORDS + 1)],
    "customer_id": cust_ids[idx],
    "customer_name": cust_name[idx],
    "customer_age": cust_age[idx],
    "customer_gender": cust_gender[idx],
    "province": cust_province[idx],
    "account_type": cust_account[idx],
    "transaction_date": ts.date,
    "transaction_time": ts.strftime("%H:%M:%S"),
    "channel": channel,
    "merchant_category": category,
    "card_type": card_type,
    "amount": amount,
    "currency": "PAB",
    "is_international": is_international,
    "status": status,
    "is_fraud": is_fraud,
})

print(f"Escribiendo {OUTPUT_FILE}...")
df.to_csv(OUTPUT_FILE, index=False)
print("Listo.")
print(f"  Registros: {len(df):,}")
print(f"  Clientes unicos: {df['customer_id'].nunique():,}")
print(f"  Transacciones marcadas como fraude: {df['is_fraud'].sum():,} "
      f"({100 * df['is_fraud'].mean():.3f}%)")
print(f"  Rango de montos: {df['amount'].min()} - {df['amount'].max()} PAB")
