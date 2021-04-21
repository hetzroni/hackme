import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    EXAMPLE_FIELD = "World"
    NEXT_URL_HEADER = "Next-URL"

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
