import os


def get_db_config():
    return {
        'username': os.getenv("POSTGRES_USERNAME"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'database': os.getenv("POSTGRES_DATABASE"),
        'host': os.getenv("POSTGRES_HOST"),
        'port': os.getenv("POSTGRES_PORT")
    }
