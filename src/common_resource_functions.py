#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from pandas import DataFrame, isna, option_context

from src.protocols import ResourceHandler


class CommonResourceFunctions:
    attached_resource: ResourceHandler

    def __init__(self, resource: ResourceHandler):
        self.attached_resource = resource
        self.errors: list[str] = []
        self.errors_count: int = 0

    def run_common_validations(self) -> list[str] | None:
        self.check_attached_resource_input_data()
        self.check_empty_input_data(self.attached_resource.input_data)
        required_fields = self.attached_resource.required_fields
        self.check_missing_required_fields(required_fields)
        self.check_missing_values_in_required_fields(required_fields)
        self.check_all_cells_characters()

        if self.errors_count > 0:
            self.raise_validation_errors()

    def raise_validation_errors(self) -> None:
        if self.errors_count > 0:
            msg = "- " + "\n- ".join(self.errors)
            raise ValueError(f"Detected {self.errors_count} problem(s):\n{msg}")

    def check_missing_required_fields(self, required_fields: list[str]) -> list | None:
        current_fields = [str(fld) for fld in self.attached_resource.input_data.columns]
        missing_required_fields = set(required_fields) - set(current_fields)
        if missing_required_fields:
            msg = "Missing required field(s):\n"
            for missing_field in missing_required_fields:
                self._remove_missing_field_to_continue_validations(missing_field)
                self.errors_count += 1
                msg += f"   - {missing_field}\n"
            self.errors.append(msg)

    def _remove_missing_field_to_continue_validations(self, missing_field: str) -> None:
        self.attached_resource.required_fields.remove(missing_field)

    def check_missing_values_in_required_fields(
        self, required_fields: list[str]
    ) -> list[str] | None:
        missing_data: dict[str, list[str]] = {}
        for field_label in required_fields:
            for idx, value in self.attached_resource.input_data[field_label].items():
                if value != "" or not isinstance(value, str) and value is not None:
                    continue

                human_idx = int(str(idx)) + 2  # +2: +1 for 0-idx +1 for headers row
                error = f"Row {human_idx}"
                if field_label not in missing_data:
                    missing_data[field_label] = []
                missing_data[field_label].append(error)

        if not missing_data:
            return

        msg = "Missing data in mandatory fields:\n"
        for idx, value in missing_data.items():
            self.errors_count += 1
            msg += f"  - Column '{idx}':\n"
            for err in value:
                msg += f"    - {err}\n"
        self.errors.append(msg)

    def check_all_cells_characters(self) -> list[str]:
        for label, content in self.attached_resource.input_data.items():
            for index, value in content.items():
                cell_problems = self.validate_cell_characters(label, index, value)
                if cell_problems:
                    self.errors_count += 1
                    self.errors.append(cell_problems)

    def check_attached_resource_input_data(self) -> None:
        if (
            not hasattr(self.attached_resource, "input_data")
            or self.attached_resource.input_data is None
        ):
            raise Exception("Missing input_data. Try 'load_input_data' first.")

    def check_empty_input_data(self, data: DataFrame) -> None:
        if data.empty and "manage" in data.columns:
            msg = "No rows with data to manage. Check the manage column and enable some rows."
            raise ValueError(msg)
        if data.empty:
            raise ValueError("No rows with data to insert have been found.")

    def validate_cell_characters(self, label: str, index: int, value) -> str | None:
        if value is None or isna(value):
            return
        if not isinstance(value, str) or value == "":
            return

        for validator in [
            self.search_invalid_characters,
            self.validate_first_and_last_characters,
        ]:
            invalid_characters = validator(label, index, value)
            if invalid_characters:
                return invalid_characters

    def search_invalid_characters(
        self, label: str, index: int, value: str
    ) -> str | None:
        invalid_chars: list[str] = ["\t", "−", "–", "–"]
        if any(element in value for element in invalid_chars):
            human_row = int(index) + 2  # + 1 for 0-idx and + 1 for header row
            return f"Invalid character in column '{label}' row '{human_row}'."

    def validate_first_and_last_characters(
        self, label: str, index: int, value: str
    ) -> str | None:
        invalid_first_and_last_chars = [" ", "\n"]

        first_char: str = value[0]
        last_char: str = value[-1]
        if first_char in invalid_first_and_last_chars:
            human_row = int(index) + 2  # + 1 for 0-idx and + 1 for header row
            return (
                f"Invalid first char: '{value}' in column '{label}' row '{human_row}'."
            )
        if last_char in invalid_first_and_last_chars:
            human_row = int(index) + 2  # + 1 for 0-idx and + 1 for header row
            return (
                f"Invalid last char: '{value}' in column '{label}' row '{human_row}'."
            )
