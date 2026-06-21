import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Geo_file_updated.xlsx")

df["bmi"] = pd.to_numeric(df["bim"], errors="coerce")

df["bmi_group"] = df["bmi"].apply(
    lambda x: "Healthy" if x <= 24.9 else "Overweight_Obese"
)

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

    "Espaços Públicos \n e Comerciais ": [
        "public_building",
        "industrial_building",
        "commercial_building",
        "retail_space"
    ]
}

all_space_cols = []

for cols in space_profiles.values():
    all_space_cols.extend(cols)

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

for col in all_space_cols:
    df[col] = df[col] / df["n_spaces"]

def compute_profiles(df_subset):

    results = {}

    for profile, cols in space_profiles.items():
        results[profile] = df_subset[cols].sum().sum()

    temp = pd.DataFrame({
        "Perfil": results.keys(),
        "Score": results.values()
    })

    temp["Percentage"] = (
        temp["Score"] / len(df_subset)
    ) * 100

    return temp

df_healthy = df[df["bmi_group"] == "Healthy"]
df_over = df[df["bmi_group"] == "Overweight_Obese"]

healthy_df = compute_profiles(df_healthy)
over_df = compute_profiles(df_over)

final_df = healthy_df[["Perfil", "Percentage"]].merge(
    over_df[["Perfil", "Percentage"]],
    on="Perfil",
    suffixes=("_Healthy", "_Overweight")
)

final_df["Mean"] = (
    final_df["Percentage_Healthy"] +
    final_df["Percentage_Overweight"]
) / 2

final_df = final_df.sort_values(
    by="Mean",
    ascending=False
)

#Gráfico 

x = range(len(final_df))

plt.figure(figsize=(12,6))

# Peso Adequado = verde
bars1 = plt.bar(
    [i - 0.2 for i in x],
    final_df["Percentage_Healthy"],
    width=0.4,
    color="#68aa67",
    alpha=0.6,
    label="Peso Adequado"
)

# Excesso de Peso e Obesidade = vermelho
bars2 = plt.bar(
    [i + 0.2 for i in x],
    final_df["Percentage_Overweight"],
    width=0.4,
    color="#f06565",
    alpha=0.6,
    label="Excesso de Peso e Obesidade"
)

plt.xticks(
    x,
    final_df["Perfil"],
    rotation=20,
    fontsize=14
)

plt.yticks(fontsize=14)

plt.ylabel(
    "Percentagem (%)",
    fontsize=14
)

plt.title(
    "Frequência de Utilização dos Espaços por Perfil de IMC",
    fontsize=14
)

plt.legend(fontsize=14)

for bar in bars1:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f"{height:.1f}%",
        ha='center',
        va='bottom',
        fontsize=12
    )

for bar in bars2:
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
