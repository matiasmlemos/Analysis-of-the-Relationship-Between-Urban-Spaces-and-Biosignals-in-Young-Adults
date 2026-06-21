import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("participants-file-com-bmi.xlsx")

df["bmi"] = pd.to_numeric(df["bmi"], errors="coerce")

# Categorias de BMI
def bmi_category(bmi):
    if bmi <= 18.5:
        return "Baixo Peso"
    elif bmi <= 24.9:
        return "Peso Normal"
    elif bmi <= 29.9:
        return "Excesso de Peso"
    elif bmi <= 34.9:
        return "Obesidade 1"
    elif bmi <= 39.9:
        return "Obesidade 2"
    else:
        return "Obesidade 3"

df["bmi_category"] = df["bmi"].apply(bmi_category)

df["gender"] = df["gender"].astype(str).str.strip().str.lower()

counts = df.groupby(["bmi_category", "gender"]).size().unstack(fill_value=0)

order = [
    "Baixo Peso",
    "Peso Normal",
    "Excesso de Peso",
    "Obesidade 1",
    "Obesidade 2",
    "Obesidade 3"
]

counts = counts.reindex(order)

x = np.arange(len(counts.index))
width = 0.35

plt.figure(figsize=(10,6))

plt.bar(
    x - width/2,
    counts.get("male", 0),
    width,
    label="Masculino",
    color="lightskyblue"
)

plt.bar(
    x + width/2,
    counts.get("female", 0),
    width,
    label="Feminino",
    color="pink"
)

plt.xlabel("Categoria de IMC", fontsize=14)
plt.ylabel("Número de Indivíduos", fontsize=14)
plt.title("Distribuição da Amostra por IMC e Género", fontsize=14)

plt.xticks(x, counts.index, rotation=45, fontsize=14)
plt.yticks(fontsize=14)

plt.legend(fontsize=14)

for i, v in enumerate(counts.get("male", [])):
    plt.text(
        i - width/2,
        v + 0.1,
        str(v),
        ha='center',
        fontsize=12
    )

for i, v in enumerate(counts.get("female", [])):
    plt.text(
        i + width/2,
        v + 0.1,
        str(v),
        ha='center',
        fontsize=12
    )

plt.tight_layout()
plt.show()
