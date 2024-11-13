# Analyse et Prédiction de Playlists Spotify

Ce projet Python permet d'analyser et de prédire certaines caractéristiques des playlists Spotify, en se basant sur un ensemble de fichiers JSON contenant des informations de playlists. Il offre plusieurs analyses et visualisations des données, et utilise des arbres de décision pour estimer si une playlist est collaborative, et pour prédire le nombre de followers des playlists.

Pour l'exemple de ce TP j'ai uniquement utiliser 1000 playlists au format JSON dans un fichier sur le million proposé dans le dataset officiel suivant : <a href="https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge">Spotify Million Playlist Dataset Challenge</a>.<br />
Bien entendu il est possible de mettre tous les fichiers data de playlist pour <b>~ 32 GB</b> dans le dossier ```./data```

Voici l'exemple de la structure d'un JSON pour une seule playlist : 
```json
{
        "name": "musical",
        "collaborative": "false",
        "pid": 5,
        "modified_at": 1493424000,
        "num_albums": 7,
        "num_tracks": 12,
        "num_followers": 1,
        "num_edits": 2,
        "duration_ms": 2657366,
        "num_artists": 6,
        "tracks": [
            {
                "pos": 0,
                "artist_name": "Degiheugi",
                "track_uri": "spotify:track:7vqa3sDmtEaVJ2gcvxtRID",
                "artist_uri": "spotify:artist:3V2paBXEoZIAhfZRJmo2jL",
                "track_name": "Finalement",
                "album_uri": "spotify:album:2KrRMJ9z7Xjoz1Az4O6UML",
                "duration_ms": 166264,
                "album_name": "Dancing Chords and Fireflies"
            },
//.................................................
        ],

    }
```

## Structure du Projet

- **Bibliothèques Utilisées** : `pandas`, `glob`, `os`, `json`, `matplotlib.pyplot`, `sklearn.tree`, `seaborn`.
- **Visualisations** : Graphiques de répartition des playlists selon le nombre de titres, albums, et artistes.
- **Modèles de Machine Learning** : Arbre de décision pour estimer la probabilité de collaboration et prédire le nombre de followers.

## Fonctionnalités

1. **Chargement et Préparation des Données**  
   - Les fichiers JSON sont lus et les données des playlists sont aplaties pour simplifier leur utilisation.
   - Les données sont chargées dans un `DataFrame` Pandas pour une manipulation facile.

2. **Analyse Exploratoire des Données**  
   - Calcul du pourcentage de playlists collaboratives et du nombre moyen de titres pour les playlists collaboratives et non-collaboratives.
   - Visualisation des relations entre le nombre de titres, d'albums, et d'artistes des playlists.
   - Création de graphiques de dispersion et de heatmaps pour illustrer la densité de ces relations.

3. **Modèle d'Arbre de Décision pour la Collaboration**  
   - Utilise un arbre de décision pour estimer si une playlist est collaborative en fonction de trois caractéristiques : nombre de titres, d'albums, et d'artistes.
   - Affichage visuel de l'arbre de décision avec `plot_tree` pour interpréter facilement les résultats.

4. **Modèle de Prédiction pour le Nombre de Followers**  
   - Utilise un arbre de décision pour prédire le nombre de followers des playlists à partir des mêmes caractéristiques.
   - Importance des caractéristiques et score du modèle sont affichés pour interpréter la performance du modèle.

5. **Recherche d'Artistes dans les Playlists**  
   - Permet de rechercher les playlists contenant un artiste spécifique en analysant les noms d'artistes associés aux titres des playlists.
   - Retourne le nombre de playlists uniques contenant l'artiste recherché.

## Instructions

### Pré-requis

Assurez-vous d'avoir les bibliothèques suivantes installées :

```bash
pip install pandas matplotlib seaborn scikit-learn
```
