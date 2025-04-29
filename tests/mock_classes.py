#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict

from pandas import DataFrame, read_pickle

from src.protocols import DataBaseHandler, ImporterHandler

PICKLES_DIR = Path("tests/files")


class MockDBHandler:
    def set_credentials(self, **credentials) -> None: ...
    def connect_with_db(self) -> None: ...
    def close_db_connection(self, rollback: bool = False) -> None: ...
    def insert_resource_data(self, resource_name: str, data: DataFrame) -> None: ...
    def load_resource_data(self, resource_name: str, data: DataFrame) -> DataFrame: ...


class MockImporter:
    def load_data(
        source: str | bytes,
        section: int | str | None = None,
        types: Dict | None = None,
    ) -> DataFrame:
        # TODO: Get a real datasheet/DataFrame and export the pickle
        return read_pickle(PICKLES_DIR / "mock_resource_data.pickle")


class MockResource:
    data_importer: ImporterHandler
    db_data: DataFrame
    db_handler: DataBaseHandler
    expected_input_data_format: dict[str, type]
    input_data: DataFrame
    required_fields: list[str]
    resource_name: str = "MockResource"
    section: int | str = "MockResource"
    validated_data: bool = False

    def __init__(self, resource_sheet_name: str): ...
    def insert_data(self) -> None: ...
    def load_db_data(self) -> None: ...
    def load_input_data(self, source: str | bytes) -> None: ...
    def set_db_handler(self, db_handler: DataBaseHandler) -> None: ...
    def set_input_handler(self, data_importer: ImporterHandler) -> None: ...
    def show_db_data(self) -> DataFrame | None: ...
    def show_input_data(self) -> DataFrame | None: ...
    def validate_data(self) -> None: ...
