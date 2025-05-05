#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.common_resource_functions import CommonResourceFunctions
from src.xlsx_importer import XlsxImporter
from tests.mock_classes import MockResource


def test_validate_extra_spaces() -> None:
    case_filename = "tests/files/common_validations.xlsx"
    case_section = "trailing_space"
    expected = (
        "Detected 1 problem(s):\n"
        "- Invalid last char: 'Trailing_space ' in column 'col_with_error' row '4'"
    )

    importer = XlsxImporter()
    mock_res = MockResource("mock")
    mock_res.resource_name = case_filename
    mock_res.section = case_section
    validator = CommonResourceFunctions(mock_res)
    mock_res.input_data = importer.load_data(case_filename, case_section)
    with pytest.raises(ValueError) as error:
        validator.run_common_validations()

    output = error.value.args[0]
    assert expected == output
