import pandas as pd

# Étape 1 : Lire le fichier
df = pd.read_csv('df_test.csv')

# Séparation du DataFrame
rows_important = df[df['SK_ID_CURR'].isin([373022, 156925])]
other_rows = df[~df['SK_ID_CURR'].isin([373022, 156925])]

# Étape 2 : Prendre 10% des lignes qui n'ont pas les valeurs spécifiques
n = int(0.1 * len(other_rows))
rows_sample = other_rows.sample(n)

# Étape 3 : Concaténer les lignes importantes et l'échantillon
result = pd.concat([rows_important, rows_sample], axis=0)

# Étape 4 : Sauvegarder le résultat
result.to_csv('reduced_df_test.csv', index=False)

print("Le fichier 'reduced_df_test.csv' a été créé avec succès!")
