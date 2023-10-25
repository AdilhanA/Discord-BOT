# Installation

## Préparation de l'environnement virtuel Python

Pour créer un environnement virtuel Python lancer la commande : 
`python -m venv venv`

Pour lancer l'environnement virtuel, lancer la commande :
- Sur Windows : `.\venv\Scripts\activate`
- Sur Linux : `source .\venv\Scripts\activate`

Pour installer les dépendances Python du bot, lancer la commande :
`pip install -r .\requirements.txt`

## Préparation du fichier .env

- Renommer le fichier **default_env** en **.env**
- Remplacer la variable **DISCORD_TOKEN** par la valeur de votre token