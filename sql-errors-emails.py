from app.engine import SQLErrors
from app.mail import Mailer
import os


if __name__ == "__main__":
    se = SQLErrors(
        sql_server=os.environ.get("SQL_SERVER"),
        sql_user=os.environ.get("SQL_USER"),
        sql_password=os.environ.get("SQL_PASSWORD"),
        sql_db=os.environ.get("SQL_DB"),
    )

    mail = Mailer()
    error_list = se.get_todays_errors()
    error_tuple = se.parse_errors(error_list)

    for error in error_tuple:
        se.log_last_error_key(error.ErrorKey)

        mail.send_error_email(message=error, to=os.environ.get("TO_EMAIL"))
