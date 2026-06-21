import pandas as pd
from scipy.stats import pearsonr

# Ler o ficheiro usado para o heatmap
df = pd.read_excel("features_heat_map.xlsx")

# Selecionar apenas as variáveis do heatmap
vars_heatmap = ["hr", "rmssd", "valence_value", "arousal_value", "stress_value", "mets", "steps"]

df = df[vars_heatmap]

# Garantir que são valores numéricos
df = df.apply(pd.to_numeric, errors="coerce")

# Pares com maior interesse, com base no heatmap
pairs = [
    ("valence_value", "arousal_value"),
    ("valence_value", "stress_value"),
    ("mets", "steps"),
    ("arousal_value", "mets"),
    ("arousal_value", "steps"),
    ("hr", "rmssd")
]

# Calcular correlação e p-value
results = []

for var1, var2 in pairs:
    temp = df[[var1, var2]].dropna()
    
    r, p = pearsonr(temp[var1], temp[var2])
    
    results.append({
        "Variável 1": var1,
        "Variável 2": var2,
        "r": round(r, 3),
        "p-value": round(p, 5),
        "n": len(temp)
    })

results_df = pd.DataFrame(results)

print(results_df)

# Guardar resultados em Excel
results_df.to_excel("p_values_correlacoes.xlsx", index=False)