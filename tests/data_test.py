import logging
from pathlib import Path

from flask import json, url_for


resources = Path(__file__).parent / "resources"

LOGGER = logging.getLogger(__name__)


def test_individuals(app, client):
    with app.app_context():
        response = client.get(
            url_for("data.get_individuals"),
        )

        assert response.status_code == 200

        results = json.loads(response.data)
        logging.info(results)

        for entry in results:
            for k in [
                "id",
                "createdAt",
                "individualName",
                "sex",
                "commonName",
                "binomialName",
                "description",
                "observationContext",
            ]:
                assert k in entry.keys()


def test_articles(app, client):
    with app.app_context():
        response = client.get(
            url_for("data.get_articles"),
        )

        assert response.status_code == 200

        results = json.loads(response.data)
        logging.info(results)

        for entry in results:
            for k in [
                "title",
                "content",
                "publicationDate",
                "imageUrl",
            ]:
                assert k in entry.keys()


def test_points(app, client):
    with app.app_context():
        response = client.get(
            url_for("data.get_points"),
        )

        assert response.status_code == 200

        results = json.loads(response.data)
        logging.info(results)

        for entry in results:
            for k in [
                "longitude",
                "latitude",
                "idIndividual",
                "recordTimestamp",
                "depth",
            ]:
                assert k in entry.keys()


def test_geojson(app, client):
    with app.app_context():
        response = client.get(
            url_for("data.get_geojson"),
        )

        assert response.status_code == 200

        results = json.loads(response.data)
        logging.info(results)

        for entry in results:
            for k in [
                "json",
                "idIndividual",
            ]:
                assert k in entry.keys()
