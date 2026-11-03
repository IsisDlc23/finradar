from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "transactions.csv"
DOCS = RAIZ / "docs"
IMG = DOCS / "img"


def tabla_md(df):
    filas = ["| " + " | ".join(map(str, df.columns)) + " |",
             "|" + "|".join("---" for _ in df.columns) + "|"]
    for fila in df.itertuples(index=False):
        celdas = []
        for valor in fila:
            if isinstance(valor, float):
                celdas.append(f"{valor:,.2f}")
            elif isinstance(valor, int):
                celdas.append(f"{valor:,}")
            else:
                celdas.append(str(valor))
        filas.append("| " + " | ".join(celdas) + " |")
    return "\n".join(filas)


def frecuencia(df, columna):
    tabla = df[columna].value_counts().rename_axis(columna).reset_index(name="transacciones")
    tabla["porcentaje"] = 100 * tabla["transacciones"] / len(df)
    tabla["monto_total"] = tabla[columna].map(df.groupby(columna)["amount"].sum())
    return tabla


def guardar(fig, nombre):
    IMG.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(IMG / nombre, dpi=120)
    plt.close(fig)
    return f"img/{nombre}"


def graficos(df):
    rutas = {}

    fig, ax = plt.subplots(figsize=(8, 4))
    limites = [1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    ax.hist(df["amount"], bins=limites, color="#2b5d8a", edgecolor="white")
    ax.set_xscale("log")
    ax.set_xticks(limites, [f"{x:,}" for x in limites])
    ax.axvline(df["amount"].median(), color="#c0392b", ls="--", label="Mediana")
    ax.axvline(df["amount"].mean(), color="#7f8c8d", ls=":", label="Media")
    ax.set_title("Distribucion de montos (escala logaritmica)")
    ax.set_xlabel("Monto (B/.)")
    ax.set_ylabel("Transacciones")
    ax.legend()
    rutas["histograma"] = guardar(fig, "histograma_montos.png")

    por_categoria = df.groupby("merchant_category")["amount"].sum().sort_values() / 1e6
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(por_categoria.index, por_categoria.values, color="#2b5d8a")
    ax.set_title("Monto total por categoria (millones de B/.)")
    rutas["categoria"] = guardar(fig, "monto_por_categoria.png")

    por_mes = df.groupby(df["transaction_date"].str.slice(0, 7)).size()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(por_mes.index, por_mes.values, marker="o", color="#2b5d8a")
    ax.set_ylim(0, por_mes.max() * 1.15)
    ax.set_title("Transacciones por mes")
    ax.tick_params(axis="x", rotation=45)
    rutas["mes"] = guardar(fig, "transacciones_por_mes.png")

    origen = df.groupby(df["is_international"].map({0: "Local", 1: "Internacional"}))["is_fraud"].mean() * 100
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(origen.index, origen.values, color=["#c0392b", "#2b5d8a"])
    ax.set_title("Tasa de fraude por origen (%)")
    for i, valor in enumerate(origen.values):
        ax.text(i, valor, f"{valor:.2f}", ha="center", va="bottom")
    rutas["fraude"] = guardar(fig, "fraude_por_origen.png")
    return rutas


def main():
    df = pd.read_csv(CSV, dtype={"transaction_date": str, "transaction_time": str})
    rutas = graficos(df)
    montos = df["amount"]

    columnas = pd.DataFrame({
        "columna": df.columns,
        "tipo": [str(t) for t in df.dtypes],
        "nulos": [int(n) for n in df.isna().sum()],
        "valores_distintos": [int(df[c].nunique()) for c in df.columns],
    })
    estadisticas = pd.DataFrame([
        ("Conteo", f"{len(montos):,}"),
        ("Minimo", f"{montos.min():,.2f}"),
        ("Percentil 25", f"{montos.quantile(0.25):,.2f}"),
        ("Mediana", f"{montos.median():,.2f}"),
        ("Media", f"{montos.mean():,.2f}"),
        ("Percentil 75", f"{montos.quantile(0.75):,.2f}"),
        ("Percentil 95", f"{montos.quantile(0.95):,.2f}"),
        ("Maximo", f"{montos.max():,.2f}"),
        ("Desviacion estandar", f"{montos.std():,.2f}"),
    ], columns=["estadistico", "monto"])

    tasa = df["is_fraud"].mean() * 100
    tasa_int = df.loc[df["is_international"] == 1, "is_fraud"].mean() * 100
    tasa_local = df.loc[df["is_international"] == 0, "is_fraud"].mean() * 100
    tasa_alta = df.loc[montos > 3000, "is_fraud"].mean() * 100
    top5 = montos.nlargest(int(len(df) * 0.05)).sum() / montos.sum() * 100
    por_mes = df.groupby(df["transaction_date"].str.slice(0, 7)).size()
    variacion = (por_mes.max() - por_mes.min()) / por_mes.mean() * 100
    categorias = frecuencia(df, "merchant_category")
    viajes = categorias.set_index("merchant_category").loc["Viajes"]

    texto = f"""# Analisis exploratorio de datos (EDA)

Script: `scripts/eda.py` · Datos: `data/transactions.csv`

## 1. Registros y columnas

- Registros: {len(df):,}
- Clientes unicos: {df['customer_id'].nunique():,}
- Periodo: {df['transaction_date'].min()} a {df['transaction_date'].max()}

{tabla_md(columnas)}

Valores nulos en total: {int(df.isna().sum().sum()):,}.

## 2. Distribucion de los montos

{tabla_md(estadisticas)}

![Histograma de montos]({rutas['histograma']})

## 3. Frecuencia por categoria y canal

![Monto por categoria]({rutas['categoria']})

{tabla_md(categorias)}

{tabla_md(frecuencia(df, 'channel'))}

{tabla_md(frecuencia(df, 'province'))}

## 4. Fraude (is_fraud)

- Transacciones marcadas como fraude: {int(df['is_fraud'].sum()):,} ({tasa:.3f} %)
- Internacionales: {tasa_int:.2f} % · Locales: {tasa_local:.2f} %
- Montos mayores a B/. 3,000: {tasa_alta:.2f} %

![Fraude por origen]({rutas['fraude']})

## 5. Tendencia por mes

![Transacciones por mes]({rutas['mes']})

## 6. Hallazgos

1. La media ({montos.mean():.2f}) es el doble de la mediana ({montos.median():.2f}): hay muchos montos pequenos y pocos muy altos. El 5 % de las transacciones mas grandes concentra el {top5:.1f} % del dinero.
2. Las transacciones internacionales tienen {tasa_int:.2f} % de fraude frente a {tasa_local:.2f} % de las locales, unas {tasa_int / tasa_local:.0f} veces mas.
3. Solo el {tasa:.3f} % de las transacciones es fraude, asi que las clases estan muy desbalanceadas.
4. Viajes tiene el {viajes['porcentaje']:.1f} % de las transacciones pero el {viajes['monto_total'] / montos.sum() * 100:.1f} % del dinero.
5. El volumen por mes varia solo {variacion:.1f} %, no hay una tendencia fuerte en el tiempo.
"""
    DOCS.mkdir(exist_ok=True)
    (DOCS / "eda.md").write_text(texto, encoding="utf-8")
    print("Listo: docs/eda.md")


if __name__ == "__main__":
    main()