from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import ItemSerializer
from rest_framework.views import APIView
from rest_framework import status
from .models import Items
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Avg,Count
from django.contrib.postgres.aggregates.general import ArrayAgg
from .to_json import jsonExample
from django.forms import model_to_dict

@api_view(['POST'])
def login(request):
    username=request.data.get("username")
    password=request.data.get("password")
    if username is None or password is None:
        return Response(data={"erro":"Please provide both username and password"},status=status.HTTP_400_BAD_REQUEST)

    user=authenticate(username=username,password=password)

    if user:
        token,created=Token.objects.get_or_create(user=user)
        return Response(data={"key":token.key},status=status.HTTP_200_OK)
    
    return Response(data={'error':"Invalid Credention"},status=status.HTTP_404_NOT_FOUND)

class Items(APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,]
    
    def get(self,request):
        print(request.user)
        items=Item.objects.values('states__state','category').annotate(no_of_items=Count("name"),items=ArrayAgg("name"))
        # items=Item.objects.values("category").annotate(number_of_items=Count('name'))
        # items=Item.objects.all().values('category','states__state','name')

        # items=Item.objects.values('category').annotate(items=ArrayAgg('name'))
        # items=Item.objects.values('category').annotate(num_category=Count('category'))
        print(items)
        data= list(items)
        print(data)
        # serializer=ItemSerializer(items,many=True)
        # print(serializer.data)
        return Response(data)
    
    def post(self,request):
        serializer=ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_201_CREATED)

class ItemDetail(APIView):
    permission_classes=[IsAuthenticated,]

    def get_object(self,pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            
            raise Http404
   
    def get(self,request,pk):
        item=self.get_object(pk)
        serializer=ItemSerializer(item)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        item=self.get_object(pk)
        serializer=ItemSerializer(instance=item,data=request.data)
        if serializer.is_valid():
            serializer.save()
        
            return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        
        return Response(status=status.HTTP_404_NOT_FOUND,data=serializer.errors)
    
    def delete(self,request,pk):
        item=self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

        

# @api_view(['GET'])
# def item(request):
#     items=Item.objects.all()
#     serializer=ItemSerializer(items,many=True)
#     print(serializer)
#     return Response(serializer.data)

# Create your views here.
