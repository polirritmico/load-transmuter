#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.common_resource_functions import CommonResourceFunctions
from src.xlsx_importer import XlsxImporter
from tests.mock_classes import MockResource


def test_validate_extra_spaces() -> None:
    case_section = "trailing_space"
    expected = (
        "Detected 1 problem(s):\n"
        "- Invalid last char: 'Trailing_space ' in column 'col_with_error' row '4'"
    )

    resource = MockResource("mock")
    resource.section = case_section
    validator = CommonResourceFunctions(resource)
    importer = XlsxImporter()
    resource.input_data = importer.load_data(TEST_FILE, case_section)
    with pytest.raises(ValueError) as error:
        validator.run_common_validations()

    output = error.value.args[0]
    assert expected == output
