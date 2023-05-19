import os
import subprocess
import boto3
import requests

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_LIST = [
    "covers",
    "gitea",
    "healthcheck",
    "mal_database",
    "n8n",
    "paperless",
    "shikimori",
    "smbc",
    "spotify",
    "yandex",
]


def backup():
    pg_string = os.environ["PG_CONNECTION_STRING"]

    client = boto3.client(
        's3',
        aws_access_key_id=str(os.environ["S3_KEY_ID"]),
        aws_secret_access_key=str(os.environ["S3_ACCESS_KEY"]),
        endpoint_url=str(os.environ["S3_ENDPOINT"])
    )

    base_dir = Path.cwd()
    try:
        for db in DB_LIST:
            print(f"Start {db}")
            target_file = str(base_dir / f"{db}.sql")
            subprocess.run(["pg_dump", f"{pg_string}/{db}", "-f", target_file], check=True)

            prefix = os.environ["FILE_PREFIX"]
            client.upload_file(target_file, os.environ["BUCKET_NAME"], f"{prefix}/{db}")
            if os.path.exists(target_file):
                os.remove(target_file)
    except Exception as e:
        print("Error:", e)
        requests.get(os.environ["ERROR"])
        return

    requests.get(os.environ["SUCCESS"])
    print("Finish")


if __name__ == "__main__":
    backup()
