from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServerDataSerializer
from .tasks import calculate_fan_speed
from django.views.decorators.csrf import csrf_exempt


class ServerDataView(APIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = ServerDataSerializer(data=request.data)

        if serializer.is_valid():
            serverroom_temperature = serializer.validated_data['serverroom_temperature']
            softwareroom_temperature = serializer.validated_data['softwareroom_temperature']
            serverroom_humidity = serializer.validated_data['serverroom_humidity']
            

            response_data = {
                "serverroom_temperature": serverroom_temperature,
                "softwareroom_temperature": softwareroom_temperature,
                "serverroom_humidity": serverroom_humidity,
                "message": "Data received and processed successfully"
            }

            calculate_fan_speed(response_data)

            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    pass