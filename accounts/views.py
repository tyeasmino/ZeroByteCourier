from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, UserLoginSerializer 
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from rest_framework.authtoken.models import Token 
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from officeRelated.models import Branch 


class UserRegistrationApiView(APIView):     
    serializer_class = RegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # FRONTEND_URL = "https://skillcrafter1.netlify.app"  # or use environment variables

            # confirm_link = f"{FRONTEND_URL}/accounts/active/{uid}/{token}"
            confirm_link = f"https://tailor-hub-backend.vercel.app/accounts/active/{uid}/{token}"

            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'detail': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://tailor-hub-frontend.vercel.app/login')
    else:
        return Response({'detail': 'Activation failed. The link may be invalid or expired.'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id, 'username': username})
            else:
                return Response({'error': "Invalid Credential"})
        
        return Response(serializre.errors) 

@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def user_details(request): 
    user = request.user 
    data = { 
        'user_id': user.id, 
        'username': user.username, 
        'email': user.email, 
        'first_name': user.first_name, 
        'last_name': user.last_name, 
    } 
    
    try:
        branch = Branch.objects.get(branch_incharge=request.user) 
        data['branch'] = branch.id
    except Branch.DoesNotExist:
        data['branch'] = None

    return Response(data)



@api_view(['GET'])
# @permission_classes([IsAuthenticated]) 
def all_users_details(request): 
    users = User.objects.all()
    user_data = []
    
    for user in users:
        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        try:
            branch = Branch.objects.get(branch_incharge=user) 
            data['branch'] = branch.id
        except Branch.DoesNotExist:
            data['branch'] = None
        user_data.append(data)

    return Response(user_data)



@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def userid_details(request, user_id):
    try:
        # Fetch user by ID
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=404)

    # Prepare response data
    data = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    try:
        branch = Branch.objects.get(branch_incharge=user) 
        data['branch'] = branch.id
    except Branch.DoesNotExist:
        data['branch'] = None
    return Response(data)



class UserLogoutApiView(APIView):
    def get(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass
        logout(request)
        
        return redirect('login')