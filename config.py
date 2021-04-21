import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    EXAMPLE_FIELD = "World"

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
