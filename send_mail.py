import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
from sys import argv

# Set up argument parsing to allow for command-line input
parser = argparse.ArgumentParser(description="Send an email with an attachment using Python.")
parser.add_argument('-r', '--recipient', required=True)
parser.add_argument('-s', '--subject', required=True)
parser.add_argument('-a', '--attachment', required=False)
args = parser.parse_args()

sender_email = "ashraf.8466@gmail.com"

# Create App Password in your google account and save it in a file, sender_password.txt in our case here.
def read_password_from_file(file_path):
    with open(file_path, "r") as file:
        password = file.read().strip()  # Read and remove any leading/trailing whitespace
    return password
sender_password = read_password_from_file("sender_password.txt")


# Retrieve the recipient email and subject from the parsed arguments
recipient_email = args.recipient
subject = args.subject

# Compose the body of the email, incorporating the subject into the message
body = f"""
I'd like to apply for the position of {subject},

Best Regards
"""

print("recipient     : ", recipient_email)
print("subject is    : ", subject)
print("body          : \n", body)

# Define the path to the attachment (a PDF file in this case)
cv_file = args.attachment if args.attachment else 'Ashraf-Soliman-Resume-20240722.pdf'


with open(cv_file, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {cv_file}",
)

message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
html_part = MIMEText(body)
message.attach(html_part)
message.attach(part)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, message.as_string())