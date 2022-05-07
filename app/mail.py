from collections import namedtuple
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os 
from dataclasses import dataclass
from .engine import Engine


@dataclass
class Mailer:

    SENDGRID_API_KEY: str = os.environ.get("SENDGRID_API_KEY")
    from_email: str = os.environ.get("FROM_EMAIL")


    def send_error_email(self, to: str, message : namedtuple) -> None:

        """
        Sends an email to the specified email address
        with any errors that have occurred.
        Args:
            to: The email address to send the email to.
            message: The errors to send. - This is a named tuple with
            the following fields:
                - ErrorKey - The error key.
                - ErrorMessage - The error message.
                - DateCreated - The date the error occurred.
                - UserName - The user that created the error.
                - Section - The section the error occurred in.
                - Procedure - The procedure the error occurred in.
                - JobKey - The job key.
                
        """


        
        message = Mail(
            from_email=self.from_email,
            to_emails=to,
            subject=f'An Error Has Occurred in the ETL Process - {message.ErrorKey}',
            html_content=f"""
            Hello {to},<br><br>

            An error has occurred in the ETL process at {message.DateCreated:%Y-%m-%d %H:%M:%S}.<br><br>

            Please see the following error details:<br><br>

            Job Key: {message.JobKey}<br>
            Error Key: {message.ErrorKey}<br>
            Job Procedure Name: {message.Procedure}<br>
            Job Section Name: {message.Section}<br>
            Error Message: {message.ErrorMessage}<br><br>

            Initiated By User: {message.UserName}<br><br>

            Sinerely,
            Octomar Digital.
            """
            
            )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


