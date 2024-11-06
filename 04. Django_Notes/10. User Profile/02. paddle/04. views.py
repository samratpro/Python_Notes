from django.contrib.auth.decorators import login_required
from .models import *
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaddleCheckoutSerializer
from time import sleep
import logging
logger = logging.getLogger("django")


# Purchase page where user see packages ************************
@login_required(login_url='login')
def purchase_credits(request):
      # Render the available credit packages and the Paddle client token
      credit_packages = CreditPackage.objects.all()
      paddle_token = PaddleToken.objects.first()
      return render(request, 'user/credit/purchase_credits.html', {
          'credit_packages': credit_packages,
          'paddle_token': paddle_token
      })
    

# Verify checkout with rest api request **********************
class PaddleCheckoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            serializer = PaddleCheckoutSerializer(data=request.data)
            if serializer.is_valid():
                productId = serializer.validated_data['productId']
                transaction_id = serializer.validated_data['transaction_id']
                if self.verify_paddle(transaction_id) == True:
                    credit_package = CreditPackage.objects.get(product_id=productId)
                    request.user.purchase_credit(credit_package)
                    return Response(status=status.HTTP_200_OK)
                print('serializer.errors 11 : ', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            print('serializer.errors 22: ', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def verify_paddle(self, transaction_id):
        sleep(1) # 1 second delay before request
        paddle_token = PaddleToken.objects.first()
        print('paddle_token : ', paddle_token)
        headers = {"Authorization": f"Bearer {paddle_token.api_key}",
                   "Content-Type": "application/json"
                   }
        # f"https://api.paddle.com/transactions/{transaction_id}
        response = requests.get(f"https://sandbox-api.paddle.com/transactions/{transaction_id}", 
                                headers=headers)
        print('response.status_code : ', response.status_code)
        print('response.json() : ', response.json())
        if response.status_code == 200:
            data = response.json().get('data').get('status')
            print('data : ', data)
            if data == 'paid' or data == 'completed':
                return True
            return False
        return False
