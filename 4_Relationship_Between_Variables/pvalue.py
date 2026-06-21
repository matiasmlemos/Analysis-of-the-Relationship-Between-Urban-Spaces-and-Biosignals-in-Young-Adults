import pandas as pd
from scipy.stats import pearsonr

df = pd.read_excel("features_heat_map.xlsx")

vars_heatmap = ["hr", "rmssd", "valence_value", "arousal_value", "stress_value", "mets", "steps"]

df = df[vars_heatmap]

df = df.apply(pd.to_numeric, errors="coerce")

pairs = [
    ("valence_value", "arousal_value"),
    ("valence_value", "stress_value"),
    ("mets", "steps"),
    ("arousal_value", "mets"),
    ("arousal_value", "steps"),
    ("hr", "rmssd")
]

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

results_df.to_excel("p_values_correlacoes.xlsx", index=False)
