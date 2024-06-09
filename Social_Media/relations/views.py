from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Social_Media.relations.helper import error_check_send_request
from Social_Media.models import MasterUserData, RelationTable
from rest_framework.pagination import PageNumberPagination
import re
from django.core.cache import caches


class SearchUserApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try: 
            data = request.data
            if not data.get('keyword'):
                return Response ("Keyword not provided", status = status.HTTP_412_PRECONDITION_FAILED)
            
            keyword = data.get('keyword','')
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'

            if re.match(email_pattern, keyword):
                searched_data = MasterUserData.objects.filter(email = keyword)
            else:
                searched_data = MasterUserData.objects.filter(name__icontains=keyword)
            
            if searched_data.exists():
                paginator = PageNumberPagination()
                paginator.page_size = 10
                paginated_data = paginator.paginate_queryset(searched_data, request)

                if paginated_data is not None:
                    response_data = [{'name': user.name, 'email': user.email} for user in paginated_data]
                    return paginator.get_paginated_response(response_data)
                else:
                    return Response('No User Found', status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                return Response('No User Found', status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response ("Some exception has occured", status=status.HTTP_412_PRECONDITION_FAILED)
            


class SendRequest(APIView):
    permission_classes = [IsAuthenticated]
    request_count_key = 'send_request_limit'


    def post(self, request):
        try:
            count = caches['default'].get(self.request_count_key)
            if count is None:
                count = 0
            if count >= 3:
                return Response({'error': 'Rate limit exceeded, only 3 requests per minute cab be sent!!'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            data = request.data
            error, check = error_check_send_request(data)
            if check:
                sender_email = data.get('sender_email', '')
                recipient_email = data.get('recipient_email', '')
                request_status = 'pending'

                new_request = RelationTable(email = recipient_email, relation_email_id = sender_email, status = request_status)
                new_request.save()

                count += 1
                caches['default'].set(self.request_count_key, count, timeout=60)

                return Response (
                    {
                        "request_to" : recipient_email,
                        "is_successful" : True
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response (error, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response("Some exception has occured", status = status.HTTP_412_PRECONDITION_FAILED)

class AcceptRequest(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data

            if "owners_email" not in data:
                return Response ("Account Holder's Email Not Provided", status = status.HTTP_412_PRECONDITION_FAILED)
            if "acceptance_email" not in data:
                return Response ("Acceptance Email Not Provided", status = status.HTTP_412_PRECONDITION_FAILED)
            
            owners_email = data.get("owners_email", "")
            email_to_accept = data.get("acceptance_email", "")

            accept_user_request = RelationTable.objects.filter(
                email = owners_email, 
                relation_email_id = email_to_accept, 
                status = "pending").first()
            
            if accept_user_request:
                accept_user_request.status = "accepted"
                accept_user_request.save()
                return Response (
                    {
                    "accepted_user_email" : email_to_accept,
                    "isSuccessful": True
                    },
                    status = status.HTTP_200_OK
                )
            else:
                return Response ( "Error has occured, No data found against given request body", status = status.HTTP_412_PRECONDITION_FAILED )
        except:
            return Response ("Some exception has occured", status = status.HTTP_412_PRECONDITION_FAILED)


class DeleteRequest(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            if "owners_email" not in data:
                    return Response ("Account Holder's Email Not Provided", status = status.HTTP_412_PRECONDITION_FAILED)
            if "email_to_delete" not in data:
                    return Response ("Deletion Email Not Provided", status = status.HTTP_412_PRECONDITION_FAILED)

            owners_email = data.get("owners_email", "")
            email_to_delete = data.get("email_to_delete", "")

            delete_user_request = RelationTable.objects.filter(
                email = owners_email, 
                relation_email_id = email_to_delete, 
                status = "pending").first()
            
            if delete_user_request:
                delete_user_request.delete()
                return Response(
                    {
                        "email_to_delete" : email_to_delete,
                        "isSuccessful" : True
                    },
                    status = status.HTTP_200_OK
                )
            
            else:
                return Response("Error has occured, no user found against given request data", status = status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response("Some exception has occured", status= status.HTTP_412_PRECONDITION_FAILED)

class PendingRequestList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            if "owners_email" not in data:
                return Response("Account Holder's email not provided", status = status.HTTP_412_PRECONDITION_FAILED)
            owners_email = data.get("owners_email","")
            pending_requests = RelationTable.objects.filter(email = owners_email, status = "pending")
            if pending_requests.exists():
                emails = ",".join(pending_requests.values_list('relation_email_id', flat=True))
                return Response({"emails": emails}, status=status.HTTP_200_OK)
            else:
                return Response("No pending requests found", status = status.HTTP_200_OK)
        except:
            return Response("Some exception has occured", status = status.HTTP_412_PRECONDITION_FAILED)


class FriendListApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            if "owners_email" not in data:
                return Response("Account Holder's email not provided", status = status.HTTP_412_PRECONDITION_FAILED)
            owners_email = data.get("owners_email","")
            accepted_requests = RelationTable.objects.filter(email = owners_email, status = "accepted")
            if accepted_requests.exists():
                emails = ",".join(accepted_requests.values_list('relation_email_id', flat=True))
                return Response({"friends_emails": emails}, status=status.HTTP_200_OK)
            else:
                return Response("No friends found", status = status.HTTP_200_OK)
        except:
            return Response("Some exception has occured", status = status.HTTP_412_PRECONDITION_FAILED)
