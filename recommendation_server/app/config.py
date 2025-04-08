import os
from dotenv import load_dotenv
from infisical_sdk import InfisicalSDKClient
from qdrant_client import QdrantClient
import openai

PORT = 5000
HOST = "0.0.0.0"

load_dotenv("../../.env")

client = InfisicalSDKClient(host="https://app.infisical.com")
client.auth.universal_auth.login(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
)

openai_key = client.secrets.get_secret_by_name(
    secret_name="OPENAI_API",
    project_id=os.getenv("INFISICAL_PROJECT_ID"),
    environment_slug="dev",
    secret_path="/"
)

qdrant_key = client.secrets.get_secret_by_name(
    secret_name="QDRANT_API_KEY",
    project_id=os.getenv("INFISICAL_PROJECT_ID"),
    environment_slug="dev",
    secret_path="/"
)

qdrant_url = client.secrets.get_secret_by_name(
    secret_name="QDRANT_URL",
    project_id=os.getenv("INFISICAL_PROJECT_ID"),
    environment_slug="dev",
    secret_path="/"
)

# Global instances
openai_client = openai.Client(
    api_key=openai_key.secretValue
)

qdrant_client = QdrantClient(
    url=qdrant_url.secretValue,
    api_key=qdrant_key.secretValue,
    https=True
)

collection_name = "courses_collection"
