![BannerAileronsTracker](https://github.com/user-attachments/assets/8bbf085c-3fc5-42da-9e1b-90e536bef79f)

# Portail Ailerons

### Installation & Prérequis

Le projet utilise [Poetry](https://python-poetry.org/) pour la gestion des dépendances. Poetry est un outil moderne pour la gestion des packages et des environnements virtuels en Python.

#### Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- **Python 3.7+** : Assurez-vous d'avoir une version de Python supérieure ou égale à 3.7. Vous pouvez vérifier votre version de Python en exécutant la commande suivante :
  ```bash
  python --version
  ```

- **Poetry** : Si Poetry n'est pas déjà installé sur votre machine, vous pouvez l'installer en suivant les instructions sur [le site officiel de Poetry](https://python-poetry.org/docs/#installation).

#### Installation

1. **Cloner le dépôt**

   Clonez le dépôt du projet en utilisant la commande suivante :
   ```bash
   git clone <URL_DU_REPO>
   ```
   Remplacez `<URL_DU_REPO>` par l'URL réelle du dépôt Git.

2. **Installer les dépendances**

   Accédez au répertoire du projet cloné et installez les dépendances en utilisant Poetry :
   ```bash
   cd <NOM_DU_REPERTOIRE_DU_PROJET>
   poetry install
   ```
   Cette commande installera toutes les dépendances spécifiées dans le fichier `pyproject.toml`.

3. **Lancer Poetry et l'environnement virtuel**

   Activez l'environnement virtuel géré par Poetry avec la commande suivante :
   ```bash
   poetry shell
   ```
   Cette commande vous placera dans un environnement virtuel isolé où toutes les dépendances du projet sont disponibles.
### Structure du Projet

Voici l'arborescence du projet :

```
├── ailerons_tracker_backend
│   ├── blueprints
│   │   └── static
│   ├── clients
│   ├── csv_parser
│   ├── forms
│   ├── models
│   ├── templates
│   │   └── shared
│   │       └── inputs
│   └── utils
├── migrations
│   └── versions
└── tests
    └── resources
```

#### Description des Dossiers

- **ailerons_tracker_backend** : Dossier principal du projet contenant tout le code source de l'application.

- **blueprints** : Ce dossier contient les "modules" Flask. Chaque blueprint gère des vues spécifiques et peut être imbriqué pour structurer l'API de manière modulaire.
  - **static** : Dossier pour les fichiers statiques (CSS, JavaScript, images).

- **clients** : Gère les interactions avec les clients, comme les API externes.

- **forms** : Regroupe les formulaires Flask-WTF utilisés dans l'application.

- **models** : Contient les modèles SQLAlchemy qui définissent la structure de la base de données.

- **templates** : Contient les templates Jinja2 utilisés pour générer les pages HTML.
    - **shared** : Templates partagés entre différentes parties de l'application.
      - **inputs** : Inputs communs utilisés dans différents formulaires.

- **utils** : Contient des fonctions utilitaires et des helpers pour l'application.

- **migrations** : Contient les fichiers de migration de la base de données, gérés par Alembic.
  - **versions** : Sous-dossier pour les différentes versions de migration.

- **tests** : Dossier principal pour les tests unitaires et d'intégration.
  - **resources** : Contient les ressources utilisées dans les tests (fichiers de test).

### Execution et variables d'environnement

Pour lancer l'application ou une suite de test, on utilise la commande `uv run --env-file [fichier d'environnement] [script]`
Il est nécessaire de définir quel fichier d'environnement doit être chargé, selon qu'on se trouve dans un environnement de test ou en production.

Pour lancer le serveur de dev en mode débug: `uv run --env-file .env.staging flask run --debug`.
Pour lancer une suite de tests: `uv run --env-file .env.staging pytest/mon_test.py`.

### Configuration et Lancement de l'Application

La configuration de l'application et sa création se font dans le fichier `__init__.py` du module principal.

#### Fonction `create_app`

La fonction `create_app` est une factory qui crée une instance de l'application Flask.

L'application Flask est créée:

```python
Flask(__name__, instance_relative_config=True)`. 
```

Une configuration définie par un objet est chargée:

```python
app.config.from_mapping(
  SECRET_KEY=os.getenv("APP_SECRET_KEY"),
  # URI can be found in Supabase dashboard, pwd can be reset there as well
  SQLALCHEMY_DATABASE_URI=f"postgresql://"
  f"redacted:{os.getenv('DB_PWD')}"
  "redacted",
  SERVER_NAME='127.0.0.1:5000',
  APPLICATION_ROOT='/'
)
```

La base de données et les migrations sont initialisées:

```python
db.init_app(app)
migrate.init_app(app, db)
```

Un fichier de configuration de l'instance est chargé si il existe, sauf en mode test où une configuration spécifique peut être passée:

```python
if test_config is None:
  # load the instance config, if it exists, when not testing
  app.config.from_pyfile('config.py', silent=True)
else:
  # load the test config if passed in
  app.config.from_mapping(test_config)
```

Le répertoire de l'instance est créé si nécessaire:

```python
os.makedirs(app.instance_path)`.
```

La protection CSRF est activée pour les formulaires:

```python
CSRFProtect().init_app(app)
```

Les extensions Jinja Partials sont enregistrées:

```python
register_extensions(app)`
```

Le gestionnaire de connexion est initialisé avec `login_manager.init_app(app)` et les fonctions de gestion des utilisateurs et de redirection non autorisée sont définies:

```python
@login_manager.user_loader
def load_user(user):
    app.logger.info(f"Logged: {user}")
    return User()
                                                                                        
@login_manager.unauthorized_handler
def unauthorized_handler():
    form = LoginForm()
    htmx = HTMX(current_app)
                                                                                        
    if htmx:
        return make_response(
            render_partial("login/login_section.jinja", form=form),
            push_url=url_for("portal.login.show")), 302
                                                                                        
    return render_template("base_layout.jinja", view=url_for("portal.login.show")), 302                                                                                        
```

Le blueprint principal de l'application est enregistré et activé:

```python
app.register_blueprint(portal)`.
```

La configuration des routes est affichée dans la console:

```python
app.logger.info(app.url_map)
```

### Base de Données

La connexion avec la base de données est définie dans le module `db` avec la configuration par défaut. Cette connexion est initialisée dans le fichier `__init__.py` de l'application, comme vu précédemment. La base de données utilisée est une base PostgreSQL hébergée dans le cloud par Supabase.

#### Configuration de la Base de Données

-   **Mot de Passe** : Le mot de passe de la base de données doit être défini dans une variable d'environnement. Il peut être retrouvé depuis le dashboard Supabase.
-   **URI de Connexion** : L'URI de connexion à la base de données est configurée dans l'application en utilisant les informations fournies par Supabase.

#### Modèles ORM avec SQLAlchemy

Les modèles ORM SQLAlchemy définissent les colonnes des tables en mappant des attributs Python et leurs types correspondants aux types de la base de données PostgreSQL. Voici un exemple de modèle pour la table `Picture` :
```python
""" Picture model """
from sqlalchemy import ForeignKey, Identity, Text, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column as mc, relationship as rel
from ailerons_tracker_backend.db import db

# pylint: disable=locally-disabled, not-callable

class Picture(db.Model):
    """ Picture model """

    id: Mapped[int] = mc(
        postgresql.BIGINT, 
        Identity(start=1, always=True), 
        primary_key=True, 
        unique=True
    )

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), 
        default=func.now()
    )

    url: Mapped[str] = mc(Text)

    individual: Mapped['Individual'] = rel(
        back_populates='pictures'
    )

    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, 
        ForeignKey('individual.id')
    )
 ```
 
 #### Explication du Modèle `Picture`

-   **id** : Clé primaire unique de type BIGINT. La colonne utilise une séquence automatique (Identity) pour générer des valeurs uniques.
-   **created_at** : Colonne de type TIMESTAMP avec fuseau horaire, définie avec la date et l'heure actuelles par défaut.
-   **url** : Colonne de type Text pour stocker l'URL de l'image.
-   **individual** : Relation ORM avec le modèle `Individual`, définie pour permettre l'association bidirectionnelle entre `Picture` et `Individual`.
-   **individual_id** : Clé étrangère pointant vers l'ID de la table `Individual`.

### Gestion des Migrations

Les migrations permettent de gérer les modifications du schéma de la base de données au fil du temps. Alembic est utilisé pour gérer ces migrations, assurant que la base de données reste synchronisée avec les modèles définis dans le code.

Initialiser Alembic:

    flask db init

Créer un nouveau fichier de migration avec un message descriptif:

    flask db migrate -m "description de la migration"

Appliquer les migrations et mettre à jour la base de données vers la dernière version:

    flask db upgrade

Revenir à une version précédente de la base de données:

    flask db downgrade

### Relations entre les Tables

Les relations bidirectionnelles entre les tables sont définies dans les deux modèles associés, mais seule la table "enfant" doit définir la clé étrangère.

**Accès aux Objets Associés**

Lorsque vous récupérez un objet parent via une requête, les objets enfants associés sont accessibles directement. Par exemple :

```python
individual = db.session.get_one(Individual, 1)
for picture in individual.pictures:
  print(picture.url)
```

Vous pouvez également créer et associer des objets enfants à un objet parent directement dans le code :

```python
individual = Individual()
individual.pictures.append(Picture(url="http://example.com/image.jpg"))
db.session.add(individual)
db.session.commit()
```

### Exécution des Requêtes

Vous pouvez exécuter des requêtes en utilisant SQL brut ou en générant des statements sans rédiger de SQL directement :

1. **Génération des Statements**

   Utilisez les helpers fournis par l'objet `db` pour générer des statements SQL de manière programmatique :

   ```python
   stmt = db.select(Individual).where(Individual.id == 1)
   ```

2. **Exécution**

  Utilisez la session de base de données pour exécuter le statement :

   ```python
   res = db.session.execute(stmt)
   individuals = res.scalars().all()
   ```

 Scalars retourne une liste de résultats correspondant au statement. Il est nécessaire de spécifier le format de la réponse attendue ainsi.
 
 On procède pareillement pour supprimer une entrée:

  ```python
  ind = db.session.get_one(ind, 1)
  db.session.delete(ind)
  db.session.commit()
  ```

3. **Avec pandas**

  Il est aussi possible d'insérer directement des _dataframes_ avec pandas si leur structure correspond à un modèle:
  
  ```python
    df = pd.read_csv(csv_file)
    df.to_sql(name='record', con=db.engine,
          if_exists='append', index=False)
  ```

### Authentification

L'authentification des utilisateurs est gérée grâce à l'extension Flask-Login. Actuellement, il n'est pas possible de créer de nouveaux comptes utilisateurs ; seul un compte Administrateur existe, dont le mot de passe est défini par un hash cryptographique généré à partir d'une variable d'environnement.

#### Configuration de l'Authentification

1. **Chargement de la Variable d'Environnement**

   Le mot de passe est conservé dans une variable d'environnement

   ```python

   admin_pword = os.getenv('ADMIN_PWD')

   if admin_pword is None:
       raise EnvVarError('ADMIN_PWD')
   ```

2. **Définition du Modèle Utilisateur**

   Le modèle `User` utilise Flask-Login pour gérer les sessions utilisateur et vérifie le mot de passe via un hash cryptographique :

   ```python
   class User(UserMixin):
       """ Load the default version of User class provided by flask_login and add methods """

       pwd_hash = generate_password_hash(admin_pword)
       id = 'Admin'

       @classmethod
       def check_pwd(cls, pword: str):
           """ Compare stored and provided password hash """
           return check_password_hash(pwhash=cls.pwd_hash, password=pword)
   ```

3. **Session utilisateur persistante**

   Une fois authentifié, des données et un cookie de session sont générés pour maintenir la session utilisateur persistante.

#### Contrôle d'Accès

Un gestionnaire, initialisé lors de la création de l'application, contrôle les données de session chaque fois qu'un utilisateur tente d'accéder à une vue protégée. Si l'utilisateur n'est pas authentifié, il est redirigé vers le formulaire de connexion.

Pour protéger une route, utilisez le décorateur `login_required` fourni par Flask-Login :

```python
from flask_login import login_required

@dashboard.get('/')
@login_required
def show():
    """ Serve dashboard """
    return render_template('dashboard.html')
```

### Interface Utilisateur

#### HTMX

Le front-end de l'application est géré avec HTMX, une bibliothèque JavaScript qui étend les capacités Hypermedia du HTML à tous les éléments. En d'autres termes, cela signifie que n'importe quel élément HTML peut déclencher des requêtes serveur et insérer des réponses au format HTML directement dans le DOM.

HTMX fournit des helpers permettant de définir précisément quand et comment sont exécutées les requêtes et les modifications du DOM.

#### Jinja

Les réponses HTML sont générées par Jinja2, un moteur de templates puissant qui permet la réutilisation du code, le rendu conditionnel et le rendu de listes. L'extension Jinja-Partials permet de créer des templates "partiels" qui, au lieu de correspondre à une vue complète, représentent des éléments discrets et réutilisables.

##### Avantages de ces Technologies

- HTMX permet de réaliser des clients légers en déplaçant l'essentiel de la logique côté serveur, réduisant ainsi la complexité et le temps de développement du front-end de l'application.

- La gestion de l'état de l'application est centralisée sur le serveur. L'état de la base de données est reflété précisément dans le HTML généré, ce qui simplifie la synchronisation client-serveur.

- L'absence de framework front-end lourd réduit significativement le poids de l'application. HTMX, par exemple, ne pèse que 14kb. Les temps de chargement sont plus rapides et la quantité de code exécuté dans le navigateur est réduite.

- Il n'est pas nécessaire de passer par une étape de build, ce qui facilite et accélère les déploiements.

#### Structure du Front-End de l'Application

Afin d'émuler le comportement d'une Single Page Application (SPA), l'application utilise une vue racine qui définit le layout principal :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Ailerons back-office portal" />
    <meta name="keywords" content="Ailerons, back-office, portal" />
    <link rel="stylesheet" href="{{ url_for('portal.static', filename='styles.css') }}" />
    <script src="https://unpkg.com/htmx.org@1.9.11" integrity="sha384-0gxUXCCR8yv9FM2b+U3FDbsKthCI66oH5IA9fHppQq9DDMHuMauqq1ZHBpJxQ0J0" crossorigin="anonymous"></script>
    <script defer src="{{ url_for('portal.static', filename='script.js') }}"></script>
    <title>Portail Ailerons</title>
</head>
<body>
    <header class="show" id="navbar">
        <section id="logo-section">
            <img height="auto" width="auto" id="main-logo" src="{{ url_for('portal.static', filename='Ailerons_Logo.png') }}" alt="Logo de l'association" />
            <h1>Portail Ailerons</h1>
        </section>
        <nav class="navbar">
            <li>
                <ul>
                    <a hx-get="{{ url_for('portal.login.show') }}" hx-target="main" hx-push-url="true" hx-swap="innerHTML">Connexion</a>
                </ul>
                <ul>
                    <a hx-get="{{ url_for('portal.dashboard.show') }}" hx-target="main" hx-push-url="true" hx-swap="innerHTML">Dashboard</a>
                </ul>
            </li>
        </nav>
    </header>
    <main>
        <div hx-get="{{ view }}" hx-push-url="true" hx-target="main" hx-swap="innerHTML" hx-trigger="load"></div>
    </main>
</body>
</html>
```

##### Fonctionnement

Au chargement initial de la page, les attributs HTMX présents dans l'élément `<div>` déclenchent une requête vers une vue spécifiée dans le template. Cette vue peut être une vue par défaut lors du premier chargement ou une vue spécifique lors d'un rafraîchissement manuel de la page.

Une fois la vue par défaut chargée, la navigation s'effectue via différents éléments (comme ceux présents dans la barre de navigation). Ces éléments déclenchent des requêtes qui insèrent les différentes vues dans l'élément `<main>`. Ainsi, la page entière n'est chargée qu'une seule fois, et seuls certains éléments sont modifiés, ajoutés ou retirés. Ce processus est connu sous le nom de "swapping". Un élément déclenchant une requête peut se modifier lui-même ou effectuer un swap ailleurs dans le document.

### Routing & Gestion des Vues

#### Configuration des Routes
Les différents endpoints de l'application sont exposés via des blueprints. Pour éviter les erreurs de frappe et faciliter le refactoring, il est recommandé d'utiliser la méthode `url_for()` pour générer les URLs dynamiquement. Cette méthode accepte comme argument une chaîne de caractères au format `"blueprint_parent.blueprint_enfant.fonction_de_la_vue"`, ainsi que des paramètres optionnels.

**Exemples :**
- `url_for("portal.show")` correspond à la route `"/portal/"` et à la méthode `show()` pour une requête GET.
- `url_for("portal.csv.upload", id=1)` correspond à la route `"/portal/csv/upload?id=1"` et à la méthode `upload()` pour une requête POST.

#### Gestion du Rafraîchissement et de la Navigation Manuelle
Les routes correspondant à des vues renvoient généralement des templates partiels, sans les métadonnées nécessaires au chargement des fichiers statiques ni les éléments externes à la vue. Par défaut, si la page est rechargée ou si une adresse est tapée directement dans la barre de navigation, un template partiel non fonctionnel est récupéré.

Pour éviter cela, on vérifie si la requête est une requête HTMX. Si ce n'est pas le cas, on déduit la vue rechargée à partir de l'URL et on passe cette vue au template de base (`base_layout`), que l'on renvoie ensuite.

Voici un exemple de blueprint pour le dashboard :

```python
""" Dashboard blueprint """

from jinja_partials import render_partial
from jinja2 import TemplateNotFound
from flask import Blueprint, abort, current_app, render_template, url_for
from flask_htmx import HTMX
from flask_login import login_required
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.individual_model import Individual

dashboard = Blueprint('dashboard', __name__,
                      template_folder='templates', url_prefix='/dashboard')

@dashboard.get('/')
@login_required
def show():
    """ Serve dashboard """
    htmx = HTMX(current_app)

    try:
        if htmx:
            return render_partial('dashboard/dashboard.jinja')
        return render_template('base_layout.jinja', view=url_for("dashboard.show"))

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)

@dashboard.get('/individuals')
@login_required
def show_table():
    try:
        individuals = db.session.execute(
            db.select(Individual)
        ).scalars().all()

        return render_template("dashboard/partials/individual_table.jinja", inds=individuals), 200

    except TemplateNotFound as e:
        current_app.logger.error(e)
        abort(404)
```

#### Explications

- **Blueprint** : Le blueprint `dashboard` est initialisé avec un préfixe d'URL `/dashboard` et un dossier de templates associé.
- **Route `show`** : La méthode `show` gère la route GET `/dashboard/`. Si la requête est une requête HTMX, elle renvoie un template partiel. Sinon, elle renvoie le template `base_layout` avec la vue appropriée.
- **Route `show_table`** : La méthode `show_table` gère la route GET `/dashboard/individuals`. Cette requête est déclenchée systématiquement depuis le template renvoyé par la route `show()`:

```html
<section id="dashboard">
    <h2>
        Dashboard
    </h2>
    <hr />
    {{ render_partial("map/map_preview.jinja") }}

    <table hx-get="{{ url_for("portal.dashboard.show_table") }}"
           hx-trigger="load"
           hx-swap="outerHTML"
           hx-push-url="true">
    </table>
    {{ render_partial("dashboard/partials/help.jinja") }}
    <button popovertarget="help">
        Aide
    </button>
</section>
```

Elle exécute une requête pour récupérer les objets `Individual` et les passe au template `individual_table.jinja`. Elle met à jour l'URL de la page afin de le faire correspondre à la vue. Cela permet de circonscrire le chargement des entrées de la table "individual" au blueprint dashboard, car le template en lui-même peut-être renvoyé par d'autres routes dans le cadre d'une redirection, par exemple après l'envoi réussi d'un fichier CSV:

```python
@csv.post('/upload')
@login_required
def upload():
    """ Parse a CSV file and insert data in DB """

    try:
       # ... logique de la vue
        return make_response(render_partial('dashboard/dashboard.jinja'),
                             push_url=url_for("portal.dashboard.show")), 200

```
