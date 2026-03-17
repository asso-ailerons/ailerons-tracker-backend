"""WTForms for individual and context"""

from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    RadioField,
    StringField,
    SelectField,
    TextAreaField,
)
from wtforms.fields import DateTimeLocalField
from wtforms.validators import Length, DataRequired, NumberRange


class ContextForm(FlaskForm):
    """Context form

    Fields:
        size (int): 1 <= range <= 20.
        date (datestring): %Y/%m/%d.
        situation (str): Seul, En groupe, Avec partenaire.
        behavior (str)
    """

    size = IntegerField("Envergure au balisage", [NumberRange(1, 20)])

    tag_date = DateTimeLocalField(
        "Date du balisage", [DataRequired("Veuillez renseigner la date.")]
    )

    situation = RadioField(
        choices=[
            ("Seul", "Seul"),
            ("En groupe", "En groupe"),
            ("Avec partenaire", "Avec partenaire"),
        ],
        validators=[DataRequired("Veuillez renseigner la situation.")],
    )

    behavior = TextAreaField(
        "Comportement observé",
        default="Rédigez vos observations ici",
        validators=[
            DataRequired("Veuillez renseigner le comportement observé.")
        ],
    )


class IndividualForm(FlaskForm):
    """Individual form

    Fields:
        individual_name (str): 3 <= length <= 25.
        sex (str): Male, Femelle, Inconnu.
        picture (postgreSQL Array): URLs.
        description (str)
    """

    individual_name = StringField(
        "Surnom",
        [
            DataRequired("Veuillez renseigner un surnom."),
            Length(min=3, max=25),
        ],
    )

    sex = SelectField(
        "Sexe",
        choices=[
            ("Male", "Male"),
            ("Femelle", "Femelle"),
            ("Inconnu", "Inconnu"),
        ],
        validators=[DataRequired("Veuillez renseigner le sexe.")],
    )

    description = StringField(
        "Description", [DataRequired("Veuillez renseigner une description.")]
    )
