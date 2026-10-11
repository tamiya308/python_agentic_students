import os

from dotenv import load_dotenv


def load_env():
    """Load .env.<APP_ENV> from the project root. APP_ENV defaults to "local".

    "local" points at the DynamoDB Local container; "dev" uses AWS via AWS_PROFILE.
    """
    load_dotenv(f".env.{os.getenv('APP_ENV', 'local')}")
