![BannerAileronsTracker](https://github.com/user-attachments/assets/8bbf085c-3fc5-42da-9e1b-90e536bef79f)

# Portail Ailerons

### Gestionnaire de paquets

Le projet utilise [UV](https://docs.astral.sh/uv/).

### Exécution et variables d'environnement

Pour lancer l'application ou une suite de tests, on utilise la commande `uv run --env-file [fichier d'environnement] [script]`
Il est nécessaire de définir quel fichier d'environnement doit être chargé, selon qu'on se trouve dans un environnement de test ou en production.

Pour lancer le serveur de dev en mode débug: `uv run --env-file .env.staging flask run --debug`.
Pour lancer une suite de tests: `uv run --env-file .env.staging pytest/mon_test.py`.

### Hébergement et déploiement
L'application est hébergée chez Koyeb: [ici](https://thirsty-marys-ailerons-75ee0bac.koyeb.app/). Koyeb utilise aussi UV.

#### Commande d'exécution en production
Pour que le serveur démarre l'application, la commande `web: gunicorn 'ailerons_tracker_backend:create_app()'` est renseignée dans le fichier `Procfile`. 

### Organisation et fonctionnement

La configuration de l'application et sa création se font dans le fichier `__init__.py` du module principal.
La fonction `create_app` est une factory qui crée une instance de l'application Flask.
Les différentes composantes de l'app sont organisées en `Blueprints` qui définissent des routes et contiennent et importent les fonctions dont ils dépendent.

### Base de Données

L'application utilise SQLAlchemy pour interagir avec la base de données. L'extension est créée dans le module `db.py` et fournie à l'application au démarrage. La configuration a été définie en amont avec les variables d'environnement nécessaires.

#### Modèles ORM avec SQLAlchemy

Les modèles ORM SQLAlchemy définissent les colonnes des tables en mappant des attributs Python et leurs types correspondants à ceux de PostgreSQL.

```python
class Record(Base):
    """Model for a GPS data record."""

    __tablename__ = "record"

    id: Mapped[int] = mc(
        postgresql.BIGINT,
        Identity(start=1, always=True),
        primary_key=True,
        unique=True,
    )
    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now()
    )
    latitude: Mapped[int] = mc(postgresql.FLOAT)
    longitude: Mapped[int] = mc(postgresql.FLOAT)
    point_feature: Mapped["GeoJSON"] = mc(postgresql.JSON, nullable=True)
    depth: Mapped[int] = mc(Integer, nullable=True)
    csv: Mapped["Csv"] = rel(back_populates="records")
    csv_uuid: Mapped[UUID] = mc(Uuid, ForeignKey("csv.uuid"))
    individual: Mapped["Individual"] = rel(back_populates="records")
    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey("individual.id")
    )
    record_timestamp: Mapped[str] = mc(postgresql.TIMESTAMP(timezone=False))
 ```

### Sérialisation et accès aux données

Les données sont accessibles aux apps depuis les routes définies par le Blueprint `data.py`. L'extension `Flask-Marsmallow` permet de les mettre en forme et de les sérialiser selon les spécifications requises.

#### GET `/data/individuals`
Retourne tous les individus et le contexte qui leur sont associés.
```
IndividualDto {
    id: int (ID classique),
    createdAt: string,
    individualName: string,
    sex: string,
    commonName: string,
    binomialName: string,
    description: string,
    observationContext: IndividualObservationContextDto
}

IndividualObservationContextDto {
    situation: string,
    size: number,
    behavior: string
}
```

#### GET `/data/articles`
Retourne tous les articles.

```
ArticleDto {
	title: string,
	content: string,
	publicationDate: string,
	imageUrl: string,
}
```

#### GET `/data/records/point`
Retourne tous les points de localisation.

```
RecordPointDto {
	longitude: number,
	latitude: number,
	idIndividual: number,
	recordTimestamp: string,
	depth: number?,
}
```

#### GET `/data/records/geojson`
Retourne toutes les LineStringFeatures.

```
RecordGeojsonDto {
	json: string,
	idIndividual: number,
}
```

### Gestion des Migrations

On utilise Alembic.

Initialiser Alembic:

    flask db init

Créer un nouveau fichier de migration avec un message descriptif:

    flask db migrate -m "description de la migration"

Appliquer les migrations et mettre à jour la base de données vers la dernière version:

    flask db upgrade

Revenir à une version précédente de la base de données:

    flask db downgrade

### Authentification

L'authentification des utilisateurs est gérée grâce à l'extension Flask-Login. Actuellement, il n'est pas possible de créer de nouveaux comptes utilisateurs ; seul un compte Administrateur existe, dont le mot de passe est défini par un hash cryptographique généré à partir d'une variable d'environnement.
