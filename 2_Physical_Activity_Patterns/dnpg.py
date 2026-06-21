import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("daily_activity_file_updated.xlsx")

weekday = df[df["is_weekend"] == False]["steps_diff"]
weekend = df[df["is_weekend"] == True]["steps_diff"]

plt.figure(figsize=(6,5))

plt.boxplot(
    [weekday, weekend],
    labels=["Semana", "Fim de Semana"],
    patch_artist=True,
    medianprops=dict(color="black", linewidth=2)
)

# Apenas aumento do tamanho das letras
plt.ylabel("Número de Passos", fontsize=14)
plt.title("Distribuição Geral do Número de Passos", fontsize=18)

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.show()