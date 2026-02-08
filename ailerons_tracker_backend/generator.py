"""GeoJSON generator"""

from geojson import FeatureCollection, GeoJSON
from models.individual_model import Individual
from models.feature_models import LineGeojson, to_point_feature


def generate(individual: Individual, db) -> Individual:
    """Generate GeoJSON features"""

    features: list[GeoJSON] = []

    for record in individual.records:
        point = to_point_feature(record, individual)

        record.point_feature = point

        features.append(point)

    individual.feature_collection = FeatureCollection(features)

    individual.line_feature = LineGeojson(
        individual_id=individual.id,
        geojson=LineGeojson.to_line_feature(individual.records, individual),
    )

    db.session.add(individual)
    db.session.commit()

    return individual
