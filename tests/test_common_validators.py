#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from src.common_resource_functions import CommonResourceFunctions
from src.xlsx_importer import XlsxImporter
from tests.mock_classes import MockResource

TEST_FILE: str = "tests/files/common_validations.xlsx"


def test_missing_required_value() -> None:
    case_section = "missing_required_value"
    case_required_fields = ["col_a", "col_b"]
    expected = (
        "Detected 2 problem(s):\n"
        "- Missing data in mandatory fields:\n"
        "  - Column 'col_a':\n"
        "    - Row 4\n"
        "  - Column 'col_b':\n"
        "    - Row 2\n"
    )

    resource = MockResource("mock")
    resource.section = case_section
    resource.required_fields = case_required_fields

    validator = CommonResourceFunctions(resource)
    importer = XlsxImporter()
    resource.input_data = importer.load_data(TEST_FILE, case_section)
    with pytest.raises(ValueError) as error:
        validator.run_common_validations()

    output = error.value.args[0]
    assert expected == output


def test_missing_required_fields() -> None:
    case_section = "missing_required_fields"
    case_required_fields = ["col_c"]
    expected = "Detected 1 problem(s):\n- Missing required field(s):\n   - col_c\n"

    resource = MockResource("mock")
    resource.section = case_section
    resource.required_fields = case_required_fields

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
        "- Invalid first char: ' leading space' in column 'col_b' row '3'."
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
