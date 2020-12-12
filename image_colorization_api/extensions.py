"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""

from image_colorization_api.commons.apispec import APISpecExt

apispec = APISpecExt()
