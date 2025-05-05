#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict

import gspread
from pandas import DataFrame


class GoogleSheetsImporter:
    DEFAULT_CREDENTIALS = Path(".secrets/google_credentials.json")

    def __init__(self, credentials: dict | str | None):
        if not credentials:
            credentials = str(self.DEFAULT_CREDENTIALS)

        if isinstance(credentials, str):
            try:
                credentials_path = Path(credentials)
                with open(credentials_path.absolute(), "r") as stream:
                    credentials = json.load(stream)
            except Exception:
                raise IOError("Error reading Google credentials file.")

        self.client = gspread.service_account_from_dict(credentials)

    def load_data(
        self, source: str | bytes, section: int | str, types: Dict | None = None
    ) -> DataFrame:
        try:
            self.google_sheet = self.client.open(source)
            worksheet = self.google_sheet.worksheet(section)
            data_in_sheet = worksheet.get_all_records()
            data = DataFrame(data_in_sheet)
        except Exception as err:
            raise Exception(f"Error loading the GoogleSheet:\n{err}")

        if not isinstance(data, DataFrame) or data.empty:
            msg = f"The generated DataFrame is empty after reading the file {source}."
            raise ValueError(msg)

        return data
