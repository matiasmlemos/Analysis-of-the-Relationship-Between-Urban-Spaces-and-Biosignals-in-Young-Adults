import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Geo_file_updated.xlsx")

# Definir perfis de espaço
space_profiles = {
    "Mobilidade Urbana": [
        "street_or_avenue",
        "sidewalks",
        "bus_stop",
        "car_park"
    ],

    "Espaços Residenciais": [
        "residential_building"
    ],

    "Espaços Académicos": [
        "university_or_study_space"
    ],

    "Espaços Alimentares": [
        "food_drinks_space"
    ],

    "Espaços Verdes \n e de Atividade Física": [
        "urban_green_space",
        "forest_green_space",
        "pa_space"
    ],

    "Espaços Sociais \n e Culturais": [
        "nightlife_space",
        "cultural_space"
    ],

    "Espaços Públicos \n e Comerciais": [
        "public_building",
        "industrial_building",
        "commercial_building",
        "retail_space"
    ]
}

all_space_cols = []

for cols in space_profiles.values():
    all_space_cols.extend(cols)

# Converter para 0/1
for col in all_space_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.lower()
        .eq("yes")
        .astype(int)
    )

df["n_spaces"] = df[all_space_cols].sum(axis=1)

df = df[df["n_spaces"] > 0]

# Normalizar
for col in all_space_cols:
    df[col] = df[col] / df["n_spaces"]

# Calcular perfis
profile_scores = {}

for profile, cols in space_profiles.items():
    profile_scores[profile] = df[cols].sum().sum()

profile_df = pd.DataFrame({
    "Perfil": profile_scores.keys(),
    "Score": profile_scores.values()
})

profile_df["Percentage"] = (
    profile_df["Score"] / len(df)
) * 100

# Ordenar
profile_df = profile_df.sort_values(
    by="Percentage",
    ascending=False
)

# Gráfico
plt.figure(figsize=(10,6))

bars = plt.bar(
    profile_df["Perfil"],
    profile_df["Percentage"]
)

plt.xticks(rotation=20, fontsize=14)
plt.yticks(fontsize=14)

plt.ylabel("Percentagem (%)", fontsize=14)
plt.title("Frequência de Utilização dos Espaços", fontsize=14)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.1f}%",
        ha='center',
        va='bottom',
        fontsize=12
    )

plt.tight_layout()
plt.show()
