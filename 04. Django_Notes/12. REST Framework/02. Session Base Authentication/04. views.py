from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GenerateTextSerializer


class DataView(APIView):
    def post(self, request):
        print(request.user)
        if request.user.is_authenticated:
            serializer = GenerateTextSerializer(data=request.data)
            if serializer.is_valid():
                input_text1 = serializer.validated_data['input_text1']
                input_text2 = serializer.validated_data['input_text2']
                generated_text = f"{input_text1} + {input_text2}"
                return Response({'generated_text': generated_text}, status=status.HTTP_200_OK) # This status will pass response.ok
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # This status will pass !response.ok/ not ok

