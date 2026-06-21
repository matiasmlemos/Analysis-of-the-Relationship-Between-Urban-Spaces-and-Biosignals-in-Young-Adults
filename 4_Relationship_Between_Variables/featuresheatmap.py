import pandas as pd

# ===============================
# 1. CARREGAR FICHEIROS
# ===============================
activity = pd.read_excel("activity_med.xlsx")
mood = pd.read_excel("mood_med.xlsx")
met = pd.read_excel("met_med.xlsx")
daily = pd.read_excel("daily_med.xlsx")

# ===============================
# 2. NORMALIZAR NOMES DE COLUNAS
# ===============================
# Garantir que todas têm user_id
for df in [activity, mood, met, daily]:
    df.columns = df.columns.str.strip().str.lower()

# ===============================
# 3. TRATAR DATAS (CRÍTICO!)
# ===============================

# Activity e Mood e Daily -> normalmente já têm "day"
for df in [activity, mood, daily]:
    if "day" in df.columns:
        df["day"] = pd.to_datetime(df["day"], errors="coerce").dt.date

# MET -> pode ter "date"
if "date" in met.columns:
    met["day"] = pd.to_datetime(met["date"], errors="coerce").dt.date
elif "day" in met.columns:
    met["day"] = pd.to_datetime(met["day"], errors="coerce").dt.date

# ===============================
# 4. GARANTIR NUMÉRICO
# ===============================
def convert_numeric(df):
    for col in df.columns:
        if col not in ["user_id", "day"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

activity = convert_numeric(activity)
mood = convert_numeric(mood)
met = convert_numeric(met)
daily = convert_numeric(daily)

# ===============================
# 5. AGREGAR (caso haja várias medições por dia)
# ===============================
activity = activity.groupby(["user_id", "day"]).mean().reset_index()
mood = mood.groupby(["user_id", "day"]).mean().reset_index()
met = met.groupby(["user_id", "day"]).mean().reset_index()
daily = daily.groupby(["user_id", "day"]).mean().reset_index()

# ===============================
# 6. MERGE (OUTER JOIN - MUITO IMPORTANTE)
# ===============================
df_final = activity.merge(mood, on=["user_id", "day"], how="outer")
df_final = df_final.merge(met, on=["user_id", "day"], how="outer")
df_final = df_final.merge(daily, on=["user_id", "day"], how="outer")

# ===============================
# 7. ORGANIZAR
# ===============================
df_final = df_final.sort_values(by=["user_id", "day"])

# ===============================
# 8. GUARDAR
# ===============================
df_final.to_excel("features_heat_map.xlsx", index=False)

print("Ficheiro criado com sucesso: features_heat_map.xlsx")