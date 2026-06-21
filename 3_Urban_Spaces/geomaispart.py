import pandas as pd

geo = pd.read_excel("Geo_file.xlsx")
participants = pd.read_excel("participants-file-com-bmi.xlsx")

# Selecionar apenas as colunas necessárias do participants
participants = participants[["user_id", "gender", "bmi"]]

# Garantir que user_id tem o mesmo tipo
geo["user_id"] = geo["user_id"].astype(str)
participants["user_id"] = participants["user_id"].astype(str)

geo_updated = geo.merge(participants, on="user_id", how="left")

# Renomear colunas para português
geo_updated = geo_updated.rename(columns={
    "gender": "sexo",
    "bmi": "bim"
})

geo_updated.to_excel("Geo_file_updated.xlsx", index=False)

print("Ficheiro criado com sucesso!")