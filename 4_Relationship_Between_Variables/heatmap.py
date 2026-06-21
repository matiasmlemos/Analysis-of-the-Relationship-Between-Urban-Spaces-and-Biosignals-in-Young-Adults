import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("features_heat_map.xlsx")

df = df.drop(columns=["user_id", "day"], errors="ignore")

for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.fillna(df.mean())

df_norm = (df - df.min()) / (df.max() - df.min())

corr = df_norm.corr()

plt.figure(figsize=(14, 12))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    center=0,
    fmt=".2f",
    annot_kws={"size": 10}
)

plt.title("Matriz de Correlação", fontsize=14)

plt.xticks(
    fontsize=12,
    rotation=45,
    ha="right"
)

plt.yticks(
    fontsize=12,
    rotation=0
)

# Ajustar margens
plt.subplots_adjust(
    left=0.18,
    bottom=0.20
)

plt.show()
