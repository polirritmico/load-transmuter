#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict

from pandas import DataFrame, ExcelFile, read_excel


class XlsxImporter:
    def load_data(
        self, source: str | bytes, section: int | str, types: Dict | None = None
    ) -> DataFrame:
        if isinstance(source, str) and not os.path.isfile(source):
            raise Exception(f"File not found: '{source}'")

        _types = "object" if types is None else types
        try:
            data: DataFrame = read_excel(
                source,
                sheet_name=section,
                header=0,
                engine="openpyxl",
                keep_default_na=False,
                dtype=_types,
            )
            # drop empty rows
            # data.dropna(how="all", inplace=True)
        except Exception as err:
            raise Exception("Error loading the xlsx file", err)

        if not isinstance(data, DataFrame) or data.empty:
            msg = f"The generated DataFrame is empty after reading the file {source}."
            raise Exception(msg)
        return data

    def get_sheet_names_in_xlsx_file(self, filename: str) -> list[str]:
        try:
            xlsx_file = ExcelFile(filename)
        except IOError as err:
            raise IOError(err, f"Can't read the '{filename}' file")

        # ExcelFile.sheet_names -> list[int | str], so better conver all to str
        sheet_names = [str(sheet) for sheet in xlsx_file.sheet_names]
        return sheet_names
