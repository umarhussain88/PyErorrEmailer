from dataclasses import dataclass
import os
from sqlalchemy import create_engine
import json
from collections import namedtuple


@dataclass
class Engine:

    sql_server: str
    sql_user: str
    sql_password: str
    sql_db: str

    def __post_init__(self):

        params = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={{{self.sql_server}}};DATABASE={{{self.sql_db}}};UID={{{self.sql_user}}};PWD={{{self.sql_password}}};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        con_str = f"mssql+pyodbc:///?odbc_connect={params}"
        engine = create_engine(con_str, fast_executemany=True)

        # post init
        object.__setattr__(self, "engine", engine)


@dataclass
class SQLErrors(Engine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_last_error_key(self, key: int):

        """
        Logs the last error key locally as a json file.
        Args:
            key: The last error key.
        """

        with open("last_error_key.json", "w") as f:
            key = {"key": key}
            json.dump(key, f)

    def get_todays_errors(self) -> list:

        """
        Gets latest errors from the database, that are greater than the last error key.
        Returns:
            A list of errors.
        """

        with open("last_error_key.json", "r") as f:
            last_error_file = json.load(f)
            last_error_key = last_error_file["key"]

        with self.engine.connect() as con:
            sql_string = f"""
            SELECT * FROM [etl_audit].[v_Error]
            WHERE ErrorKey > {last_error_key}
            """

            err = con.execute(sql_string)


            return err.all()

    def parse_errors(self, errors) -> namedtuple:

        """
        Parses the errors from the database.
        So that they can be sent via email.

        Args:
            errors: The errors to parse.
        Returns:
            parsed_errors: namedtuple with the following fields:
                - ErrorKey - The error key.
                - ErrorMessage - The error message.
                - DateCreated - The date the error occurred.
                - UserName - The user that created the error.
                - Section - The section the error occurred in.
                - Procedure - The procedure the error occurred in.
                - JobKey - The job key.
                - JobSeqD - The job sequence.

        """

        ErrorRecord = namedtuple(
            "ErrorRecord",
            [
                "JobKey",
                "JobSeqD",
                "Procedure",
                "Section",
                "ErrorKey",
                "ErrorMessage",
                "UserName",
                "DateCreated",
            ],
        )

        return tuple(ErrorRecord(*i) for i in errors)
