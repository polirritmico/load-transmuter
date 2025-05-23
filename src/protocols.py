#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Protocol

from pandas import DataFrame


class DataBaseHandler(Protocol):
    """Protocol defining the expected methods for database handler classes.

    Classes implementing this protocol must provide the necessary logic to
    interact with a specific database. Typically, this will include
    handlers for real databases (e.g., SQL) and mock databases for testing.

    Implementations must support credential setup, connection management,
    and basic resource data operations.
    """

    def set_credentials(self, **credentials) -> None:
        """Store all necessary credentials to establish a DB connection.

        Should be executed before `connect_with_DB`.
        """
        ...

    def connect_with_db(self) -> None:
        """Establish and store a connection with the database."""
        ...

    def close_db_connection(self, rollback: bool = False) -> None:
        """Close the active database connection.

        :param rollback: If True, rollback pending transactions before closing.
        """
        ...

    def insert_resource_data(self, resource_name: str, data: DataFrame) -> None:
        """Insert a resource's data into the database.

        :param resource_name: Identifier of the resource.
        :param data: DataFrame containing the resource data.
        """
        ...

    def load_resource_data(self, resource_name: str, data: DataFrame) -> DataFrame:
        """Load resource data from the database, selecting entries based on the given DataFrame.

        :param resource_name: The name of the resource to load from the database.
        :param data: A DataFrame containing the keys or conditions to select matching records.
        :return: A DataFrame with the loaded resource data.
        """
        ...


class ImporterHandler(Protocol):
    def load_data(
        self,
        source: str | bytes,
        section: int | str | None = None,
        types: Dict | None = None,
    ) -> DataFrame:
        """Load data from an external file.

        :param source: The source filename/url or file content as bytes to load.
        :param section: Optional section name or index to read inside the data.
        :param types: Optional expected type definitions for columns.
        :return: The loaded data as a DataFrame.
        """
        ...


class ResourceHandler(Protocol):
    """Protocol for domain resource handlers, e.g., SummaryReports, UsersList,
    etc.

    These classes manage loading, validating, and transferring data between
    external sources and the database.

    See Also: DataBaseHandler

    Fields:

    :param data_importer: The ImporterHandler used by import operations.
    :type data_importer: ImporterHandler
    :param db_data: The generated DataFrame from the DB data.
    :type db_data: DataFrame
    :param expected_input_data_format: Column/field name and the expected type.
    :type expected_input_data_format: dict: str, type
    :param input_data: The DataFrame from the input data source.
    :type input_data: DataFrame
    :param required_fields: A list of mandatory columns without empty data.
    :type required_fields: list: str
    :param resource_name: The filename, url, api, etc. of the input data source.
    :type resource_name: str
    :param section: Name or index of the section with the data inside the resource.
    :type section: int, str, None
    :param validated_data: state of the data validation. Defaults to False.
    :type validated_data: bool
    """

    data_importer: ImporterHandler
    db_data: DataFrame
    db_handler: DataBaseHandler
    expected_input_data_format: dict[str, type]
    input_data: DataFrame
    required_fields: list[str]
    resource_name: str
    section: int | str | None
    validated_data: bool = False

    def __init__(self, section: str):
        """Constructor method

        :param section: The default expected name of the resource in the datas source.
        """
        ...

    def insert_data(self) -> None:
        """Insert the processed data into the database."""

    def load_db_data(self) -> None:
        """Load resource data from the database into the object."""
        ...

    def load_input_data(self, source: str | bytes) -> None:
        """Load input data from a file using the configured importer.

        :param source: Source file path, URL, or raw data (must include extension).
        """
        ...

    def set_db_handler(self, db_handler: DataBaseHandler) -> None:
        """Set the database handler.

        :param db_handler: The database handler to use.
        """
        ...

    def set_input_handler(self, data_importer: ImporterHandler) -> None:
        """Set the data importer handler.

        :param data_importer: The importer used to load input data.
        """
        ...

    def show_db_data(self) -> DataFrame | None:
        """Display the loaded *database data* as a table, plot or other output.

        :return: The DataFrame, or None if the method outputs directly.
        """
        ...

    def show_input_data(self) -> DataFrame | None:
        """Display the loaded *input data* as a plot or table.

        :return: The DataFrame, or None if the method outputs directly.
        """
        ...

    def validate_data(self) -> None:
        """Run resource-specific tests to validate the imported data.

        This method checks the correctness of the input data.
        Tests may raise a Warning (non-fatal) for minor issues, or an Exception
        (fatal) for critical errors. Warnings should allow execution to continue,
        but must generate appropriate logs or user messages.

        :raises Warning: For non-critical validation issues that should be logged.
        :raises Exception: For critical validation failures that should stop execution.
        """
        ...
