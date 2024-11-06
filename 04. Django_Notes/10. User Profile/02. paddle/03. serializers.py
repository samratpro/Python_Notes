from rest_framework import serializers


class PaddleCheckoutSerializer(serializers.Serializer):
    productId = serializers.CharField(max_length=200)
    transaction_id = serializers.CharField(max_length=200)
