from app import SQLErrors, Mailer, logger_util
import os

logger = logger_util(__name__)

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

    if len(error_tuple) > 0:
        for error in error_tuple:
            se.log_last_error_key(error.ErrorKey)

            mail.send_error_email(message=error, to=os.environ.get("TO_EMAIL"))
    else:
        logger.info("No errors to send")