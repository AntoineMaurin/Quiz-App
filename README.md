Projet d'entraînement - Quiz_App

# Présentation

Quiz_App est une application web permettant de créer et partager des quizz, et bien sûr d'y jouer.

Il y a trois niveaux de difficulté de quizz : "easy", "medium" et "hard", représentés respectivement par les couleurs vert, jaune et rouge.
Chaque quizz peut être public ou privé, permettant ou non aux autres utilisateurs d'y participer.
Néanmoins, chaque quizz possède un code qui l'identifie, et permet de jouer des quizz privés, lorsque ce code à été partagé par son créateur.

# Fonctionnement

Le projet est réparti en 2 apps:
  -L'application racine, Quiz_App, qui contient les modèles Quiz, Question et Answer, essentiels au projet. Ses vues et urls portent sur le déroulement des quizz lorsqu'ils sont joués.
  -L'application quiz_creation, qui porte essentiellement sur la création de quizz, comme son nom l'indique. Elle ne comporte pas de modèles supplémentaires.

Une commande Django est également ajoutée au projet, qui permet d'ajouter un quizz depuis la base OpenQuizzDB (https://openquizzdb.org/index.php), à partir de la page du quizz, au format JSON.
Par exemple, si vous voulez le quizz sur les chats visible dans cette liste : https://openquizzdb.org/listing.php, sélectionnez le, puis prenez l'url du quizz au format JSON.

La commande s'utilise comme suit :
```python manage.py addquiz https://www.kiwime.com/oqdb/files/1050828847/OpenQuizzDB_050/openquizzdb_50.json```

Elle prend en paramètre cette url, qui comporte le quizz en 30 questions. Les 10 premières questions sont de la difficulté débutant, des 10 suivantes, confirmé, et les 10 dernières, de niveau expert.
Le projet crée donc 3 quizz de 10 questions, portant le même nom, mais de difficultés différentes.

# Installation

Si vous êtes simple utilisateur, vous pouvez vous rendre sur le site du projet à l'adresse suivante : https://not-really-kahoot.herokuapp.com/

Si vous voulez installer le projet chez vous, il vous faut python (version 3.8.5):

https://www.python.org/downloads/

Une fois installé, forkez ce repo dans votre espace github (bouton fork en haut à droite), puis clonez le sur votre machine à l'aide du bouton vert "Clone".

Maintenant, le projet est sur votre ordinateur, vous devez installer les dépendances pour le faire fonctionner.
Pour cela, il vous faut un gestionnaire de paquets, tel que pip : https://pip.pypa.io/en/stable/installing/

Ouvrez un terminal et rendez-vous dans votre dossier d'installation, à l'endroit où se trouve le fichier "requirements.txt".
Une fois au bon endroit, lancez la commande :
```pip install -r requirements.txt```
Cela installe les dépendances dont le projet a besoin pour fonctionner.

Vous devez également créer votre base de données postgresql ou en utiliser une existante.
Pour installer Postgres : https://www.postgresql.org/
Vous devrez ensuite renseigner les informations de connexion à votre base dans le fichier Quiz_App/settings/development.py dans la section DATABASES:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Nom de votre base de données',
        'USER': 'Nom de votre utilisateur',
        'PASSWORD': 'Votre mot de passe',
        'HOST': 'Votre hôte',
        'PORT': 'Votre port de connexion',
    }
}
```

Maintenant, vous devez créer les tables de la base de données avant de la remplir :
Lancez les commandes :

```python manage.py makemigrations```

```python manage.py migrate```

Une fois terminé,vous n'avez plus qu'à lancer le serveur de développement :
```python manage.py runserver```

Vous pouvez désormais utiliser le projet en local, généralement à l'adresse ```127.0.0.1:8000```
