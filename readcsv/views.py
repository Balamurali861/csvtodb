from rest_framework import status
from rest_framework.views import APIView
from .serializers import Userserializer, FileSerializer
from rest_framework.response import Response
from .utils import save_uploaded_file
from rest_framework.generics import GenericAPIView
from .models import File
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication,SessionAuthentication


class Signup(APIView):
    """Registers a user and returns the parameter after removing the password field(sensitive info)
    http://127.0.0.1:8000/api/register/
    Input format --> {
                        "username":"bala123",
                        "password" :"test123",
                        "is_superuser":1 or 2 (can be skipped, by default unauthenticated user will be created)
                        }
    Content-Type --> application/json"""
    @staticmethod
    def post(request):
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': 'error'}, status=status.HTTP_400_BAD_REQUEST)


class Authenticated(GenericAPIView):

    permissionclasses = [IsAuthenticated]

    @staticmethod
    def post(request):
        """Handles CSV upload
        http://127.0.0.1:8000/api/upload/?file
         Input format --> {
                            'file': 'upload_file.csv'
                            }"""

        file_save, response = save_uploaded_file(request)
        if file_save:
            return Response(response)
        else:
            return Response(response)

    @staticmethod
    def get(response):
        """Handles viewing of existing records with filters
         http://127.0.0.1:8000/api/filter/?city=Bangalore&price_min=300&price_max=10000
         Input format --> one or multiple filters
                            {
                            "date_min" : date time
                            "date_max": date time
                            "price_min": total price minimum
                            "price_max": total price maximun
                            "quantity_min": quantity minimum
                            "quantity_max": quantity maximum
                            "city": city
                            }"""

        date_min = response.GET.get('date_min', File.objects.order_by('transaction_time').values('transaction_time').first()['transaction_time'])
        date_max = response.GET.get('date_max', File.objects.order_by('transaction_time').values('transaction_time').last()['transaction_time'])
        price_min = response.GET.get('price_min',File.objects.order_by('total_price').values('total_price').first()['total_price'])
        price_max = response.GET.get('price_max',File.objects.order_by('total_price').values('total_price').last()['total_price'])
        quantity_min = response.GET.get('quantity_min', File.objects.order_by('quantity').values('quantity').first()['quantity'])
        quantity_max = response.GET.get('quantity_max',File.objects.order_by('quantity').values('quantity').last()['quantity'])
        city = response.GET.get('city', None)
        if not city:
            key_args = {
                'transaction_time__range': [date_min,date_max],
                'total_price__range': [price_min,price_max],
                'quantity__range': [quantity_min,quantity_max],
            }
        else:
            key_args = {
                'transaction_time__range': [date_min,date_max],
                'total_price__range': [price_min,price_max],
                'quantity__range': [quantity_min,quantity_max],
                'delivered_to_city':city
            }
        result = File.objects.filter(**key_args).values()
        serializer = FileSerializer(result,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request):
        """DELETES MULTIPLE OF SINGLE ENTRY BASED ON PARAMETERS GIVEN
        http://127.0.0.1:8000/api/delete/?transaction_id=5d8e2097397643fc84d68b3431bd5bb4
                 Input format --> one or multiple filters
                            {
                            "transaction_id": something
                            }"""
        body = request.GET
        key_args = {}
        for i in body:
            key_args[i] = body.get(i)
        result = File.objects.filter(**key_args).delete()
        if result[0] > 0:
            return Response(str(result[0]) + "RECORDS DELETED")
        else:
            return Response(
                "Could not complete the action , Reason: Either entry does not exist or the parameters are wrong")

class ResultExplorer(GenericAPIView):
    """Handles viewing of existing records with pagination
     http://127.0.0.1:8000/api/explorer/?page_size=20&page=2
     Input format --> {
                        'page_size': 20
                        'page:2'
                        }"""

    queryset = File.objects.all().order_by('id')
    serializer_class = FileSerializer
    pagination_class = CustomPagination

    def get(self,request,*args,**kwargs):
        try:
            paginated_queryset = self.paginate_queryset(self.get_queryset())
            if paginated_queryset is not None:
                serializer = self.serializer_class(paginated_queryset, many=True)
                serializer = self.get_paginated_response(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("Internal Server Error")
        except Exception as e:
            return Response(e)


