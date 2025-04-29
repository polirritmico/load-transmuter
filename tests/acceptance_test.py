#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

# from src.google_sheets_importer import GoogleSheetsImporter
from src.oracle8_handler import Oracle8DataBaseHandler
from src.reports_resource import ReportResource
from src.xlsx_importer import XlsxImporter
from tests.sensitive_data import (
    get_db_credentials,
    get_google_credentials,
    get_oauth_google_token,
)


@pytest.fixture
def oracledb():
    db_manager = Oracle8DataBaseHandler()
    sensitive_data = get_db_credentials()
    db_manager.set_credentials(**sensitive_data)
    yield db_manager
    db_manager.close_db_connection(rollback=True)


# @pytest.mark.skip(reason="Not implemented")
def test_insert_and_load_db_data(oracle: Oracle8DataBaseHandler) -> None:
    case = "tests/files/test_file.xlsx"
    expected_value1 = "Something"
    expected_value2 = "Some value"

    resource = ReportResource("Some_data")
    resource.set_input_handler(XlsxImporter())
    resource.set_db_handler(oracle)
    resource.load_input_data(case)
    resource.validate_data()
    resource.db_handler.connect_with_db()
    resource.insert_data()
    resource.load_db_data()

    assert not resource.db_data.empty, "Empty response"

    output_value1 = resource.db_data["value1"].iloc[0]
    output_value2 = resource.db_data["value2"].iloc[0]

    assert expected_value1 == output_value1
    assert expected_value2 == output_value2
