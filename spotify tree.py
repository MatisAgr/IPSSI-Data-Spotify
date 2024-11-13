import pandas as pd                                         # Créer et manipuler des DataFrames
import glob                                                 # Rechercher des fichiers dans un répertoire
import os                                                   # Manipuler des chemins de fichiers
import json                                                 # Lire des fichiers JSON
import matplotlib.pyplot as plt                             # Créer des graphiques
from sklearn.tree import DecisionTreeClassifier, plot_tree  # Créer un arbre de décision
import seaborn as sns                                       # Créer des graphiques

# répertoire contenant les fichiers JSON (pour l'exemple j'utilise un seul fichier)
json_dir = r'.\data'

# tous les fichiers JSON dans le répertoire
json_files = glob.glob(os.path.join(json_dir, '*.json'))

# stocker les DataFrames pour chaque fichier JSON
dataframes = []

# aplatir la structure JSON en un dictionnaire pour chaque playlist
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# lire chaque fichier JSON et l'ajouter à la liste des DataFrames
for file in json_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            flattened_data = [flatten_json(playlist) for playlist in json_data['playlists']]
            df = pd.json_normalize(flattened_data)
            dataframes.append(df)
    except (ValueError, KeyError) as e:
        print(f"Error reading {file}: {e}")


##################################################################################

combined_df = pd.concat(dataframes, ignore_index=True)

# convertir la colonne 'collaborative' en valeurs numériques ( 1 pour true et 0 pour false )
combined_df['collaborative'] = combined_df['collaborative'].apply(lambda x: 1 if x == 'true' else 0)

##################################################################################

# afficher le nombre de playlists collaboratives
num_collaborative_playlists = combined_df['collaborative'].sum()
total_playlists = len(combined_df)
print('-----------------------------------')
print(f"Number of collaborative playlists: {num_collaborative_playlists} / {total_playlists}")
print(f"Percentage of collaborative playlists: {num_collaborative_playlists / total_playlists * 100:.2f}%")
print('-----------------------------------')

##################################################################################

# calculer le nombre moyen de titres pour les playlists collaboratives et non collaboratives
avg_tracks_collaborative = combined_df[combined_df['collaborative'] == 1]['num_tracks'].mean()
avg_tracks_non_collaborative = combined_df[combined_df['collaborative'] == 0]['num_tracks'].mean()
print(f"Moyenne du nombre de titres dans les playlists collaboratives: {avg_tracks_collaborative:.2f}")
print(f"Moynne du nombre de titres dans les playlists non collaboratives: {avg_tracks_non_collaborative:.2f}")

##################################################################################

# arbre de décision pour prédire si une playlist est collaborative ou non
X = combined_df[['num_tracks', 'num_albums', 'num_artists']]
y = combined_df['collaborative']

# Créer un classificateur d'arbre de décision
clf = DecisionTreeClassifier(random_state=0)

# Adapter le classificateur aux données
clf.fit(X, y)

# Afficher l'arbre de décision
plt.figure(figsize=(20, 10), dpi=1000)
plot_tree(clf, filled=True, feature_names=X.columns, class_names=['Non-collaborative', 'Collaborative'])
plt.show()

# résumé en console
print('-----------------------------------')
print("Arbre de décision pour prédire si une playlist est collaborative ou non:")
print(f"\t- Nombre de playlists: {X.shape[0]}")
print(f"\t- Nombre de features: {X.shape[1]}")
print("Importance des features:")
for feature, importance in zip(X.columns, clf.feature_importances_):
    print(f"\t- {feature}: {importance:.4f}")
print(f"Score du modèle: {clf.score(X, y):.4f}")

##################################################################################

# Scatter nombre de titres vs. nombre d'albums dans les playlists
plt.figure(figsize=(10, 6))
plt.scatter(combined_df['num_tracks'], combined_df['num_albums'], alpha=0.5)
plt.axhline(y=combined_df['num_albums'].median(), color='r', linestyle='--', label='Médiane des albums')
plt.axvline(x=combined_df['num_tracks'].median(), color='b', linestyle='--', label='Médiane des titres')
plt.title('Nombre de titres vs. nombre d\'albums dans les playlists')
plt.xlabel('Nombre de titres')
plt.ylabel('Nombre d\'albums')
plt.legend(['Playlist', 'Médiane des albums', 'Médiane des titres'])
plt.show()

# Heatmap nombre de titres vs. nombre d'albums dans les playlists
plt.figure(figsize=(10, 6))
sns.kdeplot(x=combined_df['num_tracks'], y=combined_df['num_albums'], cmap='Reds', fill=True)
plt.title('Desité du nombre de titres vs. nombre d\'albums dans les playlists')
plt.xlabel('Nombre de titres')
plt.ylabel('Nombre d\'albums')
plt.show()

##################################################################################

# Scatter nombre de titres vs. nombre d'artistes dans les playlists
plt.figure(figsize=(10, 6))
plt.scatter(combined_df['num_tracks'], combined_df['num_artists'], alpha=0.5, color='g')
plt.axhline(y=combined_df['num_artists'].median(), color='r', linestyle='--', label='Médiane des artistes')
plt.axvline(x=combined_df['num_tracks'].median(), color='b', linestyle='--', label='Médiane des titres')
plt.title('Nombre de titres vs. nombre d\'artistes dans les playlists')
plt.xlabel('Nombre de titres')
plt.ylabel('Nombre d\'artistes')
plt.legend(['Playlist', 'Médiane des artistes', 'Médiane des titres'])
plt.show()

# Heatmap nombre de titres vs. nombre d'artistes dans les playlists
plt.figure(figsize=(10, 6))
sns.kdeplot(x=combined_df['num_tracks'], y=combined_df['num_artists'], cmap='Greens', fill=True)
plt.title('Densité du nombre de titres vs. nombre d\'artistes dans les playlists')
plt.xlabel('Nombre de titres')
plt.ylabel('Nombre d\'artistes')
plt.show()

##################################################################################

# Arbre de décision pour prédire le nb de followers d'une playlist
X = combined_df[['num_tracks', 'num_albums', 'num_artists']]
y = combined_df['num_followers']

# Créer un classificateur d'arbre de décision
clf = DecisionTreeClassifier(random_state=0)

# Adapter le classificateur aux données
clf.fit(X, y)

# Afficher l'arbre de décision
plt.figure(figsize=(20, 10), dpi=1000)
plot_tree(clf, filled=True, feature_names=X.columns)
plt.show()

# résumé en console
print('-----------------------------------')
print("Résumé de l'arbre de décision pour prédire le nombre de followers d'une playlist:")
print(f"\t- Nombre de playlists: {X.shape[0]}")
print(f"\t- Nombre de features: {X.shape[1]}")
print("Importance des features:")
for feature, importance in zip(X.columns, clf.feature_importances_):
    print(f"\t- {feature}: {importance:.4f}")
print(f"Score du modèle: {clf.score(X, y):.4f}")
print('-----------------------------------')


##################################################################################

# input pour rechercher un artiste dans les playlists
artist_name = input("Entrez le nom de l'artiste à rechercher dans les playlists: ")

# rechercher et compter l'artiste dans les playlists
artist_playlists = pd.DataFrame()
for col in combined_df.columns:
    if 'tracks_' in col and 'artist_name' in col:
        temp_df = combined_df[combined_df[col].str.contains(artist_name, case=False, na=False)]
        print(f"Found {len(temp_df)} rows in column {col}")  # Debug statement
        artist_playlists = pd.concat([artist_playlists, temp_df])

# supprimer les doublons
artist_playlists = artist_playlists.drop_duplicates()

# vérifier si artist_playlists est vide
if artist_playlists.empty:
    print("Aucune playlist trouvée avec cet artiste.")
else:
    # nombre de playlists UNIQUE contenant l'artiste
    num_playlists = artist_playlists['pid'].nunique()
    print(f"Nombre d'apparition dans les playlists (UNIQUE) | {artist_name}: {num_playlists} / {total_playlists}")

