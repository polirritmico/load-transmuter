#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pandas import DataFrame

from src.google_sheets_importer import GoogleSheetsImporter
from tests.sensitive_data import get_google_credentials


@pytest.fixture
def gsheets() -> GoogleSheetsImporter:
    credentials = get_google_credentials()
    gsheets = GoogleSheetsImporter(credentials)
    return gsheets


def test_google_sheets_importer(gsheets: GoogleSheetsImporter) -> None:
    case_source = "test_gspread"
    case_section = "Some_datatypes"

    case_col_str = "target_col"
    expected_str = "This is working"
    case_col_val = "left_col"
    expected_val = 123.456

    dataframe = gsheets.load_data(case_source, case_section)

    assert isinstance(dataframe, DataFrame)
    assert expected_str == dataframe[case_col_str].iloc[0]
    assert expected_val == dataframe[case_col_val].iloc[0]


# TODO: Add tests for dates, floats, percentages.
