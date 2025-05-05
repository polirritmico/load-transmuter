#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.common_resource_functions import CommonResourceFunctions
from src.xlsx_importer import XlsxImporter
from tests.mock_classes import MockResource

TEST_FILE: str = "tests/files/common_validations.xlsx"


def test_validate_bad_characters() -> None:
    case_section = "bad_character"
    expected = "Detected 1 problem(s):\n- Invalid character in column 'col_c' row '2'."

    importer = XlsxImporter()
    resource = MockResource("mock")
    resource.section = case_section
    validator = CommonResourceFunctions(resource)
    importer = XlsxImporter()
    resource.input_data = importer.load_data(TEST_FILE, case_section)
    with pytest.raises(ValueError) as error:
        validator.run_common_validations()

    output = error.value.args[0]
    assert expected == output


def test_validate_extra_spaces() -> None:
    case_section = "trailing_space"
    expected = (
        "Detected 1 problem(s):\n"
        "- Invalid last char: 'Trailing_space ' in column 'col_with_error' row '4'."
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


def test_validate_multiple_problems() -> None:
    case_section = "multiple_problems"
    expected = (
        "Detected 2 problem(s):\n"
        "- Invalid character in column 'col_a' row '2'.\n"
        "- Invalid last char: 'Trailing_space ' in column 'col_b' row '3'."
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
