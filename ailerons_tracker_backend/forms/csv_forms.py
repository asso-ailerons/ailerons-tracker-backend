"""WTForms for individual and context"""

from flask_wtf import FlaskForm
from wtforms.fields import FileField


class CsvForm(FlaskForm):
    """Csv form

    Fields:
    """

    loc_file = FileField("Relevés de localisation")
    depth_file = FileField("Relevés de profondeur")
