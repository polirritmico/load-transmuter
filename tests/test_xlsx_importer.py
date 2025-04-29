#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest

from src.xlsx_importer import XlsxImporter

TEST_FILES = Path("tests/files")


@pytest.fixture
def xlsx_importer():
    xlsx_importer = XlsxImporter()
    return xlsx_importer


def test_xlsx_importer_read_sheet(xlsx_importer: XlsxImporter) -> None:
    case_filename = TEST_FILES / "simple.xlsx"
    case_section = "Some_Section"
    expected = "This is working"

    parsed_xlsx = xlsx_importer.load_data(case_filename, case_section)
    output = parsed_xlsx["target_col"][0]

    assert expected == output
