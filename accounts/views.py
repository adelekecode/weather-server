from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, api_view
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import *
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from django import dispatch
from .models import *
from config.weather import process_weather
from django.utils.text import slugify
from .permissions import IsAdmin

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


 
# Create your views here.



data_signal = dispatch.Signal()



User = get_user_model()




class UserViewSet(viewsets.ModelViewSet):


    serializer_class = UserSerializer
    queryset = User.objects.filter().order_by('-date_joined')
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'role']

    def get_object(self):

        try:
            user = User.objects.get(id=self.kwargs['pk'])
        except User.DoesNotExist:
            raise NotFound("aswear user not found")
        
        return user

        

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(**serializer.validated_data)
            except Exception as e:
                return Response({"message": str(e)})
            
            data = {
                "message": "User created successfully",
            }

            data_signal.send(sender=user, data=data)
       
            
            return Response(data, status=200)
        return Response(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object()
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():

            if 'email' in data:
                return Response({"message": "You can't update email"}, status=400)
            
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors)





@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view(['POST'])
def user_login(request):

    
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)

            if user:
                if user.is_active==True:
                
                    try:
                        
                        refresh = RefreshToken.for_user(user)

                        user_detail = {}
                        user_detail['id']   = user.id
                        user_detail['email'] = user.email
                        user_detail['role'] = user.role
                        user_detail['access'] = str(refresh.access_token)
                        user_detail['refresh'] = str(refresh)
                        
                            
                        data = {
        
                            "message":"success",
                            'data' : user_detail,
                        }
             
                        return Response(data, status=status.HTTP_200_OK)
                    

                    except Exception as e:
                        raise e
                
                else:
                    data = {
                        'error': 'This account has not been activated'
                    }

                    return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    'error': 'Please provide a valid email and a password'
                }

                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                'error': serializer.errors
            }
            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            



class WeatherUpdateView(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get(self, request):


        query = request.GET.get('query', None)

        if query is None:

            all_weather = WeatherUpdate.objects.all().order_by('-created_at')

            return Response(WeatherUpdateSerializer(all_weather, many=True).data, status=200)

        

        data, status = process_weather(query)

        if status == True:


            slug = slugify(data['location']['name'])

            try:
                weather = WeatherUpdate.objects.get(slug=slug)

                weather.location = data['location']
                weather.current = data['current']
                weather.save()

                return Response(WeatherUpdateSerializer(weather).data)


            except WeatherUpdate.DoesNotExist:

                weather = WeatherUpdate.objects.create(

                    country = data['location']['name'],
                    location = data['location'],
                    current = data['current']


                )

                return  Response(WeatherUpdateSerializer(weather).data, status=200)
            
        else:
            return Response(data, status=400)

        

