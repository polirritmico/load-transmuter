#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import os
import pathlib

SECRETS_DIR: pathlib.Path = pathlib.Path("tests/.secrets")


def get_db_credentials() -> dict[str, str | None]:
    """Get the DB credentials and host info to make the DB connection

    If the tests are running in a CI environment, the function will get the
    values from env variables. Else, if the test is running in a local machine
    the function will get the values from the `staging_db_credentials` files in
    the `SECRETS_DIR`.

    :return: A dictionary with the DB credentials
    """
    if not os.environ.get("CI"):
        target_db_credentials = SECRETS_DIR / "staging_db_credentials.json"
        assert target_db_credentials.exists(), "Missing staging_db_credentials.json"

        with open(target_db_credentials, "r") as stream:
            credentials = json.load(stream)
        return credentials

    credentials = {
        "host": os.environ.get("CI_DB_HOST"),
        "port": os.environ.get("CI_DB_PORT"),
        "database": os.environ.get("CI_DB_NAME"),
        "user": os.environ.get("CI_DB_USER"),
        "password": os.environ.get("CI_DB_PASSWORD"),
    }
    return credentials


def get_google_credentials() -> dict[str, str] | str:
    """Get Google service account credentials.

    If the tests are running in a CI environment, the function will get the
    values from env variables. Else, if the test is running in a local machine
    the function will get the values from the `google_credentials.json" file in
    the `SECRETS_DIR`.

    :return: A dict with the google credentials.
    """
    if not os.environ.get("CI"):
        return str(SECRETS_DIR / "google_credentials.json")

    # The key need to be decoded (cause is a multiline string).
    # Steps to decode:
    # Encoded input env str -> encoded bin -> decoded bin -> decoded str key
    key: str = str(os.environ.get("GOOGLE_PRIVATE_KEY")).encode("ascii")
    decoded_key = base64.b64decode(key).decode("ascii")
    credentials = {
        "auth_provider_x509_cert_url": os.environ.get("GOOGLE_AUTH_PROVIDER"),
        "auth_uri": os.environ.get("GOOGLE_AUTH_URI"),
        "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
        "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
        "client_x509_cert_url": os.environ.get("GOOGLE_CLIENT_CERT_URL"),
        "private_key": decoded_key,
        "private_key_id": os.environ.get("GOOGLE_PRIVATE_KEY_ID"),
        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
        "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
        "type": os.environ.get("GOOGLE_TYPE"),
    }
    return credentials


def get_oauth_google_token() -> dict[str, str] | str:
    """Get Google OAuth2 credentials.

    If the tests are running in a CI environment, the function will get the
    values from env variables. Else, if the test is running in a local machine
    the function will get the values from the `google_token.json" file in
    the `SECRETS_DIR`.

    :return: A dict with the google oauth2 credentials
    """
    if not os.environ.get("CI"):
        return SECRETS_DIR / "google_token.json"
    credentials = {
        "token": os.environ.get("GOOGLE_TOKEN"),
        "refresh_token": os.environ.get("GOOGLE_REFRESH_TOKEN"),
        "token_uri": os.environ.get("GOOGLE_TOKEN_URI"),
        "client_id": os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
        "scopes": os.environ.get("GOOGLE_SCOPES", "").split(","),
    }
    return credentials
