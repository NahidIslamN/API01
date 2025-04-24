from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework import viewsets

from .serializers import UserSerializer, loginserializer, ProductSerializer

from django.contrib.auth import login, logout, authenticate

from django.views  import View

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Products
from rest_framework.authtoken.models import Token

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.

class Homepage(View):
    @method_decorator(login_required)
    def get(self, request):
        token = Token.objects.get(user = request.user)
        cp = {
            "token": token
            }
        return render(request, 'index.html', context=cp)




#api views here....



class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        user = request.user
        products = Products.objects.filter(oner = user ).order_by('-created_at')
        serializers = ProductSerializer(products, many = True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        datas = request.data
        datas['oner'] = request.user.id
        serializer = ProductSerializer(data = datas)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            product = Products.objects.get(id = request.data['id']) 
        except Products.DoesNotExist:
            return Response({"status":"not ok","error":"Product Object not found!"})
        
        user = request.user
        if product.oner == user:
            data = request.data
            data['oner'] = request.user.id

            serializer = ProductSerializer(instance = product, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response("you are not the owner of the product!", status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            product = Products.objects.get(id = request.data['id']) 
        except Products.DoesNotExist:
            return Response({"status":"not ok","error":"Product Object not found!"})
        
        user = request.user
        if product.oner == user:
            product.delete()
            return Response({
                "status":"OK",
                "success":"Delete Successfully"
            }, status = status.HTTP_200_OK)
            
        return Response("you are not the owner of the product!", status = status.HTTP_400_BAD_REQUEST)




       



class userregisterview(APIView):

    def post(self, request):
        user = UserSerializer(data = request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class userlogin(APIView):

    def post(self, request):
        serializers = loginserializer(data = request.data)
        if serializers.is_valid():
            user = authenticate(username = request.data['username'], password = request.data['password'])
            if user:
                login(request, user)
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:            
                return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
            
            
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


        