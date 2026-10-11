"""Drop the StudentEnrolments table for the current APP_ENV.

Run on demand from the project root: .\\tools\\DropTableLocal.ps1 or .\\tools\\DropTableDev.ps1
"""

import os

from src.config import load_env
from src.db import TABLE_NAME, configure_db, delete_table_if_exists


def check_target(env: str):
    """Stop a leftover DynamoDbUrl from sending the drop to the wrong database."""
    url = os.getenv("DynamoDbUrl")
    if env == "local" and not url:
        raise SystemExit(
            "DynamoDbUrl is not set, so this would drop the table on AWS. "
            "Check .env.local; nothing dropped."
        )
    if env == "dev" and url:
        raise SystemExit(
            f"DynamoDbUrl is set ({url}), so this would drop the local table, not AWS. "
            "Run `Remove-Item env:DynamoDbUrl` and try again; nothing dropped."
        )


def describe_target() -> str:
    url = os.getenv("DynamoDbUrl")
    if url:
        return url
    profile = os.getenv("AWS_PROFILE", "default")
    return f"AWS (profile {profile}, region {os.getenv('AWS_REGION')})"


def main():
    env = os.getenv("APP_ENV", "local")
    load_env()
    check_target(env)
    configure_db()
    target = describe_target()
    if delete_table_if_exists():
        print(f"Dropped {TABLE_NAME} from {target}.")
    else:
        print(f"{TABLE_NAME} doesn't exist in {target}; nothing dropped.")


if __name__ == "__main__":
    main()
