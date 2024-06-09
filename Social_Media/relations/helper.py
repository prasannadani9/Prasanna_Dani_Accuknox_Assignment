from rest_framework.response import Response
from rest_framework import status
from Social_Media.models import MasterUserData, RelationTable


def error_check_send_request(data):
    if "recipient_email" not in data:
        return "Recipient's Email Not Provided", False
    if "sender_email" not in data:
        "Sender's Email Not Provided", False

    recipient_email = data.get("recipient_email", "")
    master_user_emails = MasterUserData.objects.filter(email = recipient_email)
    if not master_user_emails:
        return "Recipient is not a valid user, can't find entry in User's Master Database", False
    else:
        return " ", True
