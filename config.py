import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    NEXT_URL_HEADER = "Next-Url"
    NEW_SESSION_ID_HEADER =  "Session-Id"
    NUM_SESSIONS = 50
    NUM_URLS = 10
    RANDOM_URL_LENGTH = 8

class ProductionConfig(Config):
    NUM_SESSIONS = 1_000_000


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    NUM_URLS = 2
