from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from . import helper
from rest_framework.permissions import AllowAny
from Social_Media.models import MasterUserData

class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        try:
            email = data.get('email')
            password = data.get('password')
            error_check, error_msg = helper.check_for_error_login_api(data)
            if error_check:
                user = authenticate(username=email, password=password)
                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response ({'error' : error_msg}, status = status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response({'error' : 'Exception Occured'}, status = status.HTTP_412_PRECONDITION_FAILED)

class SignupAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        try: 
            name = data.get('name', '')
            email = data.get('email','')
            password = data.get('password','')
            error_check, error_msg = helper.check_for_error_signup_api(data)
            if error_check:
                user = User.objects.create_user(username=email, password=password)
                token = Token.objects.create(user=user)

                master_user_data = MasterUserData(email = email, name = name)
                master_user_data.save()

                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error' : error_msg}, status = status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response({'error' : "Exception Occured"}, status = status.HTTP_412_PRECONDITION_FAILED)
        