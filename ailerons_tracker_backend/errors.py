"""Custom exception classes."""


class CloudinaryError(Exception):
    """Generic Cloudinary error"""

    def __init__(self, base_error):
        self.message = "Something went wrong while uploading images"
        self.base_error = base_error


class InvalidFile(Exception):
    """Invalid file name"""

    def __init__(self, base_error):
        self.message = "Could not parse file"
        self.base_error = base_error


class GeneratorError(Exception):
    """Generic GeoJSON generator error"""

    def __init__(self, base_error: Exception | None = None):
        self.message = "Something went wrong while generating geoJSONs"
        self.base_error = base_error


class GeneratorPointError(GeneratorError):
    """Error building PointFeatures"""

    def __init__(self, obj, base_error: Exception | None = None):
        super().__init__(base_error)
        self.message = (
            f"Something went wrong while generating PointFeatures with {obj}"
        )


class GeneratorLineError(GeneratorError):
    """Invalid file name"""

    def __init__(self, obj, base_error: Exception | None = None):
        super().__init__(base_error)
        self.message = (
            f"Something went wrong while generating LineFeatures with {obj}"
        )


class ParserError(Exception):
    """Invalid file name"""

    def __init__(self):
        self.message = "Something went wrong while parsing CSV file"


class EnvVarError(Exception):
    """Environment variable not set or accessed properly"""

    def __init__(self, env_var_name: str) -> None:
        self.message = f"Could not access environment variable: {env_var_name}"


class MissingParamError(Exception):
    """Missing parameter in request"""

    def __init__(self, param_name: str) -> None:
        self.message = f"Missing parameter {param_name} in request"
