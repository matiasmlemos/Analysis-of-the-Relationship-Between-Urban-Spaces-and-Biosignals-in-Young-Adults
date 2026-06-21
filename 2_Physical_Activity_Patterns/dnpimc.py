import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("daily_activity_file_gender_bim.xlsx")

# Criar grupos de BMI
df["bmi_group"] = df["user_bmi"].apply(
    lambda x: "Peso Adequado" if x <= 24.9 else "Excesso de Peso e Obesidade"
)

# Dados

healthy_week = df[
    (df["bmi_group"] == "Peso Adequado") &
    (df["is_weekend"] == False)
]["steps_diff"]

healthy_weekend = df[
    (df["bmi_group"] == "Peso Adequado") &
    (df["is_weekend"] == True)
]["steps_diff"]

over_week = df[
    (df["bmi_group"] == "Excesso de Peso e Obesidade") &
    (df["is_weekend"] == False)
]["steps_diff"]

over_weekend = df[
    (df["bmi_group"] == "Excesso de Peso e Obesidade") &
    (df["is_weekend"] == True)
]["steps_diff"]

data = [healthy_week, healthy_weekend, over_week, over_weekend]

# Boxplot

fig, ax = plt.subplots(figsize=(10,6))

bp = ax.boxplot(
    data,
    patch_artist=True,
    labels=[
        "Semana",
        "Fim de Semana",
        "Semana",
        "Fim de Semana"
    ],
    medianprops=dict(color='black', linewidth=2)
)

colors = ["green", "green", "red", "red"]

for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)

# Apenas aumento das letras
ax.set_ylabel("Número de Passos", fontsize=14)
ax.set_title("Distribuição do Número de Passos por Perfil de IMC", fontsize=14)

ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)

ax.grid(axis='y', linestyle='--', alpha=0.5)

import matplotlib.patches as mpatches

green_patch = mpatches.Patch(color='green', alpha=0.6, label='Peso Adequado')
red_patch = mpatches.Patch(color='red', alpha=0.6, label='Excesso de Peso e Obesidade')

ax.legend(
    handles=[green_patch, red_patch],
    fontsize=14
)

plt.show()