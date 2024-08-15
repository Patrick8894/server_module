from dotenv import load_dotenv
import os

ENV_FILE = os.getenv("ENV_FILE", "prod")

print(f"ENV_FILE: {ENV_FILE}")

abs_path = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(abs_path, "../env/", f"{ENV_FILE}.env")

load_dotenv(dotenv_path=env_path)

ENV = os.getenv("ENV", "PROD")

TEST_ENV = ["DEV", "QAT", "UAT"]

DB_NAME = os.getenv("DB_NAME", "my_db")

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")

MONGO_PORT = os.getenv("MONGO_PORT", 27017)