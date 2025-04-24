from rest_framework import serializers
from .models import Products
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def validate(self, data):

        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError("username already exist!")
        

        if User.objects.filter(email = data['email']).exists():

            raise serializers.ValidationError("eamil already exist!")
            
            




        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']

        )
        user.save()

        token = Token.objects.create(user = user)
        token.save()


        return validated_data
    


class loginserializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"


        