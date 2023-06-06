import csv
import pandas as pd
import os

# Chemin du fichier CSV
csv_file_path = 'bdd_series_modifie.csv'

def trier(csv_file_path):
    # Chemin du nouveau fichier CSV
    new_csv_file_path = 'nouveau_fichier12.csv'
    
    # Colonnes à conserver
    columns_to_keep = ['ID', 'recommendations']
    
    # Ouvrir le fichier d'entrée en lecture
    with open(csv_file_path, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, delimiter=';')
        fieldnames = reader.fieldnames
        
        # Créer une liste de dictionnaires pour stocker les lignes à conserver avec les colonnes étendues
        rows_extended = []
        
        # Obtenir le nombre maximum de recommandations
        max_recommendations = 0
        
        # Parcourir chaque ligne du fichier d'entrée
        for row in reader:
            # Supprimer les colonnes inutiles et conserver les colonnes spécifiées
            new_row = {column: row[column] for column in columns_to_keep}
            
            # Étendre les recommandations en colonnes individuelles
            recommendations = row["recommendations"].split(",")
            max_recommendations = max(max_recommendations, len(recommendations))
            for i, recommendation in enumerate(recommendations, start=1):
                column_name = f"recommendation{i}"
                new_row[column_name] = recommendation
            
            rows_extended.append(new_row)
    
    # Obtenir la liste des noms de colonnes étendues
    extended_fieldnames = columns_to_keep + [f"recommendation{i}" for i in range(1, max_recommendations + 1)]
    
    # Écrire les lignes avec les colonnes étendues dans un nouveau fichier CSV de sortie
    with open(new_csv_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=extended_fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows_extended)
    
    print("Les colonnes ont été supprimées et les recommandations ont été triées avec succès.")
    print("Le fichier de sortie est prêt :", new_csv_file_path)
    print("Les colonnes du fichier de sortie :", extended_fieldnames)

trier(csv_file_path)

def modifier_csv(new_csv_file_path):
    # Charger le fichier CSV en utilisant pandas
    df = pd.read_csv(new_csv_file_path, delimiter=';')
    
    # Créer une liste vide pour stocker les nouvelles lignes
    new_rows = []
    
    # Parcourir chaque ligne du DataFrame
    for _, row in df.iterrows():
        recommendations = str(row['recommendations']).split(',')  # Convertir en str et séparer les recommandations
        
        # Créer une nouvelle ligne pour chaque recommandation
        for recommendation in recommendations:
            new_row = {
                'ID': row['ID'],
                'recommendation': recommendation.strip()  # Supprimer les espaces en début et fin de chaque recommandation
            }
            new_rows.append(new_row)
    
    # Créer un nouveau DataFrame à partir des nouvelles lignes
    new_df = pd.DataFrame(new_rows)
    
    # Enregistrer le DataFrame modifié dans un nouveau fichier CSV
    new_csv_file_path1 = 'nouveau_fichier.csv'
    new_df.to_csv(new_csv_file_path1, index=False, sep=';')
    
    print("Le fichier a été modifié avec succès. Le fichier de sortie est prêt :", new_csv_file_path1)


modifier_csv('nouveau_fichier12.csv')


# Supprimer le fichier "nouveau_fichier.csv"
os.remove('nouveau_fichier12.csv')
