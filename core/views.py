from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.
def login_view(request):
    return render(request, 'users/login.html')

def home(request):

    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def source(request):

    return render(request, 'core/base.html')

class HomeDataView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] # Fixed typo: permission_classes

    def get(self, request):
        content = {
            'message': f'Welcome back, {request.user.email}!',
            'status': 'Login Successful'
        }
        return Response(content)

def root_redirect(request):
    return render(request, 'core/base.html')
